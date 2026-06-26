#!/usr/bin/env python3
"""
FINAL comprehensive Q&A extraction and merging.
Combines:
  1. _parsed_unique.json (90 questions, cleanest text)
  2. questions.json (53 questions with correct answers + explanations)
  3. Fresh extraction from all 5 text files with broader patterns
  4. Deduplication and merging of correct answers
"""

import re
import json
import os
from difflib import SequenceMatcher

BASE_DIR = r"C:\Users\david\python\cert-salesforce"

SOURCE_FILES = [
    ("Set 1 (1)_extraido.txt", "Set 1"),
    ("Revise 1_Set 2_81_extraido.txt", "Set 2"),
    ("Revise 2_Set 3_extraido.txt", "Set 3"),
    ("Read Second_Set 4_82__extraido.txt", "Set 4"),
    ("estudio_2026_v2_extracted.txt", "Estudio"),
]


def clean_ocr_text(text):
    """Aggressive cleaning of OCR noise."""
    # Page markers
    text = re.sub(r'---\s*PÁGINA\s*\d+\s*---', '\n§BREAK§\n', text)
    # Headers
    for pat in [
        r'Salesforce Certified Identity and Access Management Archite[^\n]*',
        r'Salesrorce Certiried Laentity[^\n]*',
        r'Serssiviee Verse[^\n]*',
        r'Sesser ee Corse[^\n]*',
        r'DaIESIUICE CETUNeU[^\n]*',
        r'Time Remaining[^\n]*',
        r'Time Rem[:\s]*$',
        r'kryterion[^\n]*',
        r'by\s+[DO]RAKE\s+INTERNATIONAL[^\n]*',
        r'@kryterion[^\n]*',
    ]:
        text = re.sub(pat, '', text, flags=re.IGNORECASE | re.MULTILINE)
    # Markers
    for pat in [
        r'[©OM]?\s*Ma?[er]k this item[^\n]*',
        r'Translation Value:.*?responses\.?',
        r'Press the "Pr[n]t Scrn"[^\n]*',
        r'TF?\)?\s*Mark this item[^\n]*',
    ]:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)
    # Noise words
    for pat in [r'\{?\s*(?:snow|Hide|show|stow)\s*\}?', r'€ED', r'Ss\s*(?:sr|On|oo|a|Or)\s*\)?',
                r'eg\s+Ss\s+ed\)', r'ry\s+ree', r'=a\s*(?:ae\s*Eas)?',
                r'Re\s+GS\s+SSE\s+SSS', r'SS\s+oo\s+oo', r'\(Ee\)\s*\[EES\]\s*Sea\]\s*Basa',
                r'ES\s+ES\s+ED\s+EI', r'Fos\s+J\s+next>[^\n]*']:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)
    # OCR char fixes
    text = text.replace('€.', 'C.').replace('¢.', 'C.')
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\xa0', ' ')
    return text


def split_by_question_boundaries(text, source_name):
    """Split text into question blocks by detecting boundaries."""
    
    if source_name == "Estudio":
        return split_estudio(text)
    
    # For Sets 1-4: find all "N of 64" patterns (allowing garbled numbers)
    # Pattern accepts: digits, or 1-4 garbled chars before "of/or/ot/oF 64."
    boundary_pattern = re.compile(
        r'(?:^|\n)\s*'
        r'(?:'
        r'(\d{1,2})\s+of\s+64'         # Clean: "N of 64"
        r'|'
        r'(?:\{?\d{1,2}\}?)\s+of\s+64'  # {N} of 64
        r'|'
        r'.{1,4}(?:of|or|ot|oF)\s*64'   # Garbled: "Bor 64", "eo 64", etc.
        r'|'
        r'(?:^|\n)\s*(\d{1,2})\s*of\s+64' # N of 64 at line start
        r')'
        r'\s*\.',
        re.MULTILINE
    )
    
    matches = list(boundary_pattern.finditer(text))
    
    # Also find standalone "N of 64." where N is a clean digit
    clean_pattern = re.compile(r'(?:^|\n)\s*(\d{1,2})\s+of\s+64\s*\.', re.MULTILINE)
    clean_matches = list(clean_pattern.finditer(text))
    
    # Merge all matches, sort by position, remove near-duplicates
    all_positions = set()
    for m in matches + clean_matches:
        pos = m.start()
        # Check no existing position is within 20 chars
        if not any(abs(pos - p) < 20 for p in all_positions):
            all_positions.add(pos)
    
    positions = sorted(all_positions)
    
    # Create blocks
    blocks = []
    for i, pos in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        block = text[pos:end].strip()
        if len(block) > 30:
            blocks.append(block)
    
    return blocks


def split_estudio(text):
    """Split estudio text by question numbers."""
    # Clean double-spaced text
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        if re.match(r'^[\s]*[A-Za-z]\s{2,}[A-Za-z]\s{2,}', line):
            line = re.sub(r'(?<=\S)\s{2,}(?=\S)', ' ', line)
        cleaned.append(line)
    text = '\n'.join(cleaned)
    
    # Remove category headers
    for cat in ['Identity Management Concepts', 'Community \\(Partner and Customer\\)',
                'Accepting Third-Party Identity in Salesforce', 'Salesforce as an Identity Provider',
                'Salesforce Identity', 'OAuth']:
        text = re.sub(rf'\n\s*{cat}\s*\n', '\n', text)
    
    # Find question boundaries: "N." or "N of 64." at start of line
    pattern = re.compile(r'(?:^|\n)\s*(\d{1,2})(?:\s+of\s+64)?\.\s+', re.MULTILINE)
    matches = list(pattern.finditer(text))
    
    blocks = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end].strip()
        if len(block) > 30:
            blocks.append(block)
    
    return blocks


def parse_block_to_question(block, source_name):
    """Parse a text block into a question dict."""
    
    # Remove question number prefix
    block = re.sub(r'^\s*\{?\d{0,2}\}?\s*(?:of|or|ot|oF)?\s*64\s*\.?\s*', '', block)
    block = re.sub(r'^\s*\d{1,2}(?:\s+of\s+64)?\s*\.\s*', '', block)
    block = re.sub(r'^.{0,6}(?:of|or|ot|oF)\s*64\s*\.\s*', '', block)
    
    # Find options
    if source_name == "Estudio":
        return parse_estudio_block(block)
    else:
        return parse_ocr_block(block)


def parse_ocr_block(block):
    """Parse a question block from OCR text."""
    
    # Find options: look for A., B., C., D., E. at line starts
    # Must handle: "A.Q", "A.©", "A.@", "A.(", "A oO", etc.
    opt_pattern = re.compile(
        r'(?:^|\n)\s*([A-Ea-e])\s*[\.\)]\s*'
        r'((?:(?!(?:^|\n)\s*[A-Ea-e]\s*[\.\)]).)*)' ,
        re.DOTALL | re.MULTILINE
    )
    
    opt_matches = list(opt_pattern.finditer(block))
    
    if len(opt_matches) < 3:  # Most questions have at least A,B,C,D
        return None
    
    # Question text = everything before first option
    q_text = block[:opt_matches[0].start()].strip()
    q_text = re.sub(r'\n+', ' ', q_text)
    q_text = re.sub(r'\s+', ' ', q_text)
    q_text = re.sub(r'^§BREAK§\s*', '', q_text)
    q_text = q_text.strip()
    
    if len(q_text) < 20:
        return None
    
    # "Choose N answers"
    choose_match = re.search(r'[Cc]hoos[^\n]*?(\d+)\s+answers?', q_text)
    num_answers = int(choose_match.group(1)) if choose_match else 1
    
    options = {}
    correct = []
    
    for om in opt_matches:
        letter = om.group(1).upper()
        raw = om.group(2).strip()
        
        # Detect correct answer from markers
        is_correct = False
        full_prefix = om.group(0)[:25]
        
        # Check for @ or © markers near the letter
        if re.search(rf'{letter}\s*[\.\)]\s*[@©®]', full_prefix, re.IGNORECASE):
            is_correct = True
        if re.search(rf'{letter}\s*[\.\)]\s*@@', full_prefix, re.IGNORECASE):
            is_correct = True
        if re.match(r'^[@©®]\s', raw):
            is_correct = True
        if re.match(r'^@@\s', raw):
            is_correct = True
        if re.match(r'^\(\s*[@©]\s*\)', raw):
            is_correct = True
        
        # Special patterns: "D.@" "c©" etc. in the full match
        if re.search(rf'{letter}\.@\s', full_prefix):
            is_correct = True
        if re.search(rf'{letter}©', full_prefix):
            is_correct = True
        if re.search(rf'{letter}\s*\.\s*\(@\)', full_prefix):
            is_correct = True
        
        # Check for "5@", "x)", "EX)" markers
        if re.match(r'^[x5s]\)', raw[:5]):
            is_correct = True
        if re.match(r'^EX\)', raw[:5]):
            is_correct = True
        
        # Clean option text
        clean = raw
        # Remove leading markers
        for p in [r'^[@©®]\s*', r'^@@\s*', r'^\(\s*[@©PpB]\s*\)\s*', r'^\(\s*\)\s*',
                  r'^[oO]\s+[oO]\s+', r'^[oO©]\s+[oO©]\s+', r'^Oo\s+', r'^oO\s+',
                  r'^[Cc][yY]\s+', r'^[iI]C\s+', r'^ee\s+', r'^c\)\s+', r'^t\)\s+',
                  r'^[x5s]\)\s*', r'^EX\)\s*', r'^Q\s+', r'^O\s+(?=[A-Z])',
                  r'^D\s+(?=[A-Z])', r'^\[e\)\s*', r'^\(\s*P\s*\)\s*',
                  r'^G@\s*', r'^G\.\(\s*', r'^Gg\)\s*']:
            clean = re.sub(p, '', clean, count=1)
        
        # Remove trailing noise
        clean = re.sub(r'\s*[@©]\s*$', '', clean)
        clean = re.sub(r'\s*§BREAK§.*$', '', clean, flags=re.DOTALL)
        
        # Collapse whitespace
        clean = re.sub(r'\n+', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean)
        clean = clean.strip(' .')
        
        if clean and len(clean) > 1:
            options[letter] = clean
            if is_correct:
                correct.append(letter)
    
    if len(options) < 3:
        return None
    
    return {
        "question": q_text,
        "options": options,
        "correct_answers": sorted(list(set(correct))),
        "num_expected_answers": num_answers,
    }


def parse_estudio_block(block):
    """Parse a question block from estudio format."""
    
    # Remove category headers
    for cat in ['Identity Management Concepts', 'Community (Partner and Customer)',
                'Accepting Third-Party Identity in Salesforce', 'Salesforce as an Identity Provider',
                'Salesforce Identity', 'OAuth']:
        block = re.sub(rf'\s*{re.escape(cat)}\s*$', '', block, flags=re.MULTILINE)
    
    # Find options: "- A." pattern
    opt_pattern = re.compile(r'[-–]\s+([A-Ea-e])\.\s+(.*?)(?=\s*[-–]\s+[A-Ea-e]\.\s|$)', re.DOTALL)
    opt_matches = list(opt_pattern.finditer(block))
    
    if len(opt_matches) < 2:
        return None
    
    q_text = block[:opt_matches[0].start()].strip()
    q_text = re.sub(r'^\s*\d{1,2}(?:\s+of\s+64)?\.\s*', '', q_text)
    q_text = re.sub(r'\n+', ' ', q_text)
    q_text = re.sub(r'\s+', ' ', q_text)
    q_text = q_text.strip()
    
    if len(q_text) < 15:
        return None
    
    choose_match = re.search(r'Choose\s+(\d+)\s+answers?', q_text, re.IGNORECASE)
    num_answers = int(choose_match.group(1)) if choose_match else 1
    
    options = {}
    correct = []
    
    for om in opt_matches:
        letter = om.group(1).upper()
        raw = om.group(2).strip()
        
        is_correct = False
        if 'Opción marcada' in raw:
            is_correct = True
            if 'pero incorrecta' in raw.lower():
                is_correct = False
            raw = re.sub(r'\s*\(?\s*Opción marcada[^)]*\)?\s*', '', raw)
        
        raw = re.sub(r'\n+', ' ', raw)
        raw = re.sub(r'\s+', ' ', raw)
        raw = raw.strip(' .')
        
        if raw and len(raw) > 1:
            options[letter] = raw
            if is_correct:
                correct.append(letter)
    
    if len(options) < 2:
        return None
    
    return {
        "question": q_text,
        "options": options,
        "correct_answers": sorted(list(set(correct))),
        "num_expected_answers": num_answers,
    }


def normalize(text):
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def similarity(a, b):
    return SequenceMatcher(None, a[:120], b[:120]).ratio()


def merge_and_dedup(all_questions):
    """Merge questions from multiple sources, keeping best version of each."""
    unique = []
    norms = []
    
    for q in all_questions:
        norm = normalize(q["question"])
        
        found = False
        for i, existing_norm in enumerate(norms):
            if similarity(norm, existing_norm) > 0.75:
                found = True
                existing = unique[i]
                # Merge correct answers
                merged_correct = list(set(existing.get("correct_answers", []) + q.get("correct_answers", [])))
                
                # Keep the version with better data
                q_score = len(q.get("correct_answers", [])) * 10 + len(q.get("options", {})) + len(q["question"]) // 10
                e_score = len(existing.get("correct_answers", [])) * 10 + len(existing.get("options", {})) + len(existing["question"]) // 10
                
                # If new has explanation, prefer it
                if q.get("explanation"):
                    q_score += 20
                if existing.get("explanation"):
                    e_score += 20
                
                if q_score > e_score:
                    q["correct_answers"] = sorted(merged_correct)
                    if existing.get("explanation") and not q.get("explanation"):
                        q["explanation"] = existing["explanation"]
                    if existing.get("concept") and not q.get("concept"):
                        q["concept"] = existing["concept"]
                    unique[i] = q
                    norms[i] = normalize(q["question"])
                else:
                    existing["correct_answers"] = sorted(merged_correct)
                    if q.get("explanation") and not existing.get("explanation"):
                        existing["explanation"] = q["explanation"]
                    if q.get("concept") and not existing.get("concept"):
                        existing["concept"] = q["concept"]
                break
        
        if not found:
            unique.append(q)
            norms.append(norm)
    
    return unique


def load_parsed_unique():
    """Load and convert _parsed_unique.json."""
    path = os.path.join(BASE_DIR, "_parsed_unique.json")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = []
    for item in data:
        options = {}
        for c in item.get("choices", []):
            options[c["id"]] = c["text"]
        
        q = {
            "question": item["stem"],
            "options": options,
            "correct_answers": item.get("marked", []),
            "num_expected_answers": item.get("choose_n", 1),
            "source": item.get("source", ""),
            "concept": item.get("concept", ""),
        }
        questions.append(q)
    
    return questions


def load_questions_json():
    """Load and convert questions.json."""
    path = os.path.join(BASE_DIR, "questions.json")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = []
    for item in data.get("questions", []):
        options = {}
        for c in item.get("choices", []):
            options[c["id"]] = c["text"]
        
        q = {
            "question": item["question"],
            "options": options,
            "correct_answers": item.get("correctAnswers", []),
            "num_expected_answers": len(item.get("correctAnswers", [])) or 1,
            "source": "questions.json",
            "concept": item.get("concept", ""),
            "explanation": item.get("explanation", ""),
        }
        questions.append(q)
    
    return questions


def extract_from_texts():
    """Extract questions from all text files."""
    all_questions = []
    
    for filename, source_name in SOURCE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        text = clean_ocr_text(text)
        blocks = split_by_question_boundaries(text, source_name)
        
        count = 0
        for block in blocks:
            parsed = parse_block_to_question(block, source_name)
            if parsed:
                parsed["source"] = source_name
                all_questions.append(parsed)
                count += 1
        
        print(f"  {source_name}: {len(blocks)} blocks -> {count} questions parsed")
    
    return all_questions


def main():
    print("Loading existing parsed data...")
    parsed_unique = load_parsed_unique()
    print(f"  _parsed_unique.json: {len(parsed_unique)} questions")
    
    questions_json = load_questions_json()
    print(f"  questions.json: {len(questions_json)} questions")
    
    print("\nExtracting from text files...")
    text_extracted = extract_from_texts()
    print(f"  Total from texts: {len(text_extracted)}")
    
    # Combine all sources - order matters for merge priority
    # questions.json first (has explanations), then parsed_unique, then text extraction
    all_questions = questions_json + parsed_unique + text_extracted
    print(f"\nTotal combined: {len(all_questions)}")
    
    # Merge and deduplicate
    print("Merging and deduplicating...")
    unique = merge_and_dedup(all_questions)
    print(f"Unique questions: {len(unique)}")
    
    # Assign IDs
    for i, q in enumerate(unique, 1):
        q["id"] = i
    
    # Stats
    with_answer = sum(1 for q in unique if q.get("correct_answers"))
    with_explanation = sum(1 for q in unique if q.get("explanation"))
    print(f"With correct answer: {with_answer}")
    print(f"With explanation: {with_explanation}")
    
    # Save JSON
    json_path = os.path.join(BASE_DIR, "_final_questions.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"\nJSON: {json_path}")
    
    # Save readable TXT
    txt_path = os.path.join(BASE_DIR, "_final_questions.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"Salesforce Identity & Access Management Architect - Question Bank\n")
        f.write(f"Total unique questions: {len(unique)}\n")
        f.write(f"With correct answer: {with_answer}\n")
        f.write(f"With explanation: {with_explanation}\n\n")
        
        for q in unique:
            f.write(f"{'='*70}\n")
            f.write(f"Q{q['id']}")
            if q.get('concept'):
                f.write(f" [{q['concept']}]")
            if q.get('num_expected_answers', 1) > 1:
                f.write(f" (Choose {q['num_expected_answers']})")
            f.write(f"\n{'='*70}\n")
            f.write(f"{q['question']}\n\n")
            for letter in sorted(q.get('options', {}).keys()):
                marker = " ✓" if letter in q.get('correct_answers', []) else ""
                f.write(f"  {letter}. {q['options'][letter]}{marker}\n")
            if q.get('correct_answers'):
                f.write(f"\n  → Correct: {', '.join(q['correct_answers'])}\n")
            else:
                f.write(f"\n  → Correct: [NOT IDENTIFIED]\n")
            if q.get('explanation'):
                f.write(f"  💡 {q['explanation']}\n")
            f.write(f"\n")
    print(f"TXT: {txt_path}")
    
    # Questions without answers
    no_ans = [q for q in unique if not q.get('correct_answers')]
    print(f"\nQuestions without answer ({len(no_ans)}):")
    for q in no_ans[:20]:
        print(f"  Q{q['id']}: {q['question'][:80]}...")


if __name__ == "__main__":
    main()
