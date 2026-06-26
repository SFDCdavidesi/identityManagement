#!/usr/bin/env python3
"""
Robust extraction of Q&A from Salesforce Identity certification exam files.
Handles two formats:
  1. OCR-extracted text from Sets 1-4 (screenshots): "N of 64." format
  2. Estudio 2026 V2 (text-based): different spacing, "(Opción marcada)" markers
"""

import re
import json
import os
from difflib import SequenceMatcher

BASE_DIR = r"C:\Users\david\python\cert-salesforce"
LOG_FILE = os.path.join(BASE_DIR, "_extraction_log.txt")

# Files to process
SOURCE_FILES = [
    ("Set 1 (1)_extraido.txt", "Set 1"),
    ("Revise 1_Set 2_81_extraido.txt", "Set 2"),
    ("Revise 2_Set 3_extraido.txt", "Set 3"),
    ("Read Second_Set 4_82__extraido.txt", "Set 4"),
    ("estudio_2026_v2_extracted.txt", "Estudio"),
]

log_lines = []

def log(msg):
    log_lines.append(msg)
    print(msg)


def clean_text(text):
    """Remove common noise from extracted text."""
    # Remove page markers
    text = re.sub(r'---\s*PÁGINA\s*\d+\s*---', '\n', text)
    # Remove exam header lines
    text = re.sub(r'Salesforce Certified Identity and Access Management Archite(?:ct)?[^\n]*', '', text)
    text = re.sub(r'Serssiviee Verse.*?\n', '', text)
    text = re.sub(r'Time Remaining[:\s]*[\d:]*[^\n]*', '', text)
    text = re.sub(r'kryterion[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'by\s+[DO]RAKE\s+INTERNATIONAL[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[©O]\s*Mark this item for later review\.?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Mark this item for later review\.?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'@kryterion[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Translation Value:.*?responses\.?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Fos\s*J\s*next>.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'previous\s*<?\s*next\s*>?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Browse.*?submit', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{?\s*snow\s*\}?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\{?\s*Hide\s*\}?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[Ss]ho\b', '', text)
    text = re.sub(r'\b[Gg]p\b', '', text)
    text = re.sub(r'\b[Gg]r\b', '', text)
    text = re.sub(r'\b@rr?\b', '', text)
    text = re.sub(r'\b@rh\b', '', text)
    text = re.sub(r'€ED', '', text)
    text = re.sub(r'[Ss]r\)', '', text)
    text = re.sub(r'\bEES\b', '', text)
    text = re.sub(r'\bBasa\b', '', text)
    text = re.sub(r'\bSea\b', '', text)
    # Unicode cleanup
    text = text.replace('\u2019', "'")
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\xa0', ' ')
    text = text.replace('€.', 'C.')  # OCR error: € -> C
    text = text.replace('¢.', 'C.')  # OCR error: ¢ -> C
    return text


def clean_estudio_text(text):
    """Clean the estudio file which has extra spacing between characters."""
    # This file has double-spaced characters in some lines
    # Remove excessive spacing within words
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # If line has many double-spaced characters, compress them
        # Pattern: single chars separated by double spaces
        if re.match(r'^[\s]*[A-Za-z]\s{2,}[A-Za-z]\s{2,}', line):
            # Compress double-spaced text
            line = re.sub(r'(?<=\S)\s{2,}(?=\S)', ' ', line)
        cleaned.append(line)
    return '\n'.join(cleaned)


def parse_sets_format(text, source_name):
    """Parse questions from Sets 1-4 format (OCR extractions)."""
    questions = []
    
    # Find question boundaries using "N of 64." pattern
    # Also handle just "N." at start of context
    q_starts = list(re.finditer(r'(?:^|\n)\s*(\d{1,2})\s+of\s+64\s*\.', text))
    
    if not q_starts:
        log(f"  WARNING: No 'N of 64.' patterns found in {source_name}")
        return questions
    
    for i, match in enumerate(q_starts):
        q_num = int(match.group(1))
        start = match.end()
        
        # End is the start of the next question, or end of text
        if i + 1 < len(q_starts):
            end = q_starts[i + 1].start()
        else:
            end = len(text)
        
        q_block = text[start:end].strip()
        
        parsed = parse_question_block(q_block, q_num, source_name)
        if parsed:
            questions.append(parsed)
        else:
            log(f"  WARN: Could not parse Q{q_num} from {source_name}")
    
    return questions


def parse_estudio_format(text, source_name):
    """Parse questions from estudio 2026 format."""
    questions = []
    
    # Clean the double-spaced text
    text = clean_estudio_text(text)
    
    # The estudio file has category headers followed by question numbers
    # Pattern: "N." or "N of 64." at beginning of a section
    q_starts = list(re.finditer(r'(?:^|\n)\s*(\d{1,2})(?:\s+of\s+64)?\s*\.\s+', text))
    
    if not q_starts:
        log(f"  WARNING: No question numbers found in {source_name}")
        return questions
    
    for i, match in enumerate(q_starts):
        q_num = int(match.group(1))
        start = match.end()
        
        if i + 1 < len(q_starts):
            end = q_starts[i + 1].start()
        else:
            end = len(text)
        
        q_block = text[start:end].strip()
        
        parsed = parse_estudio_block(q_block, q_num, source_name)
        if parsed:
            questions.append(parsed)
        else:
            log(f"  WARN: Could not parse Q{q_num} from {source_name}")
    
    return questions


def parse_estudio_block(block, q_num, source_name):
    """Parse a question block from the estudio format."""
    # Remove category headers that might be at the end
    block = re.sub(r'\n\s*(?:Identity Management Concepts|Community \(Partner and Customer\)|'
                   r'Accepting Third-Party Identity in Salesforce|Salesforce as an Identity Provider|'
                   r'Salesforce Identity|OAuth)\s*$', '', block, flags=re.MULTILINE)
    
    # Options in estudio format: "- A. text" or "- A. text (Opción marcada)"
    option_pattern = re.compile(r'[-–]\s+([A-F])\.\s+(.*?)(?=\s*[-–]\s+[A-F]\.\s|\s*$)', re.DOTALL)
    option_matches = list(option_pattern.finditer(block))
    
    if len(option_matches) < 2:
        return None
    
    # Question text is everything before the first option
    first_opt = option_matches[0]
    question_text = block[:first_opt.start()].strip()
    
    # Clean "Choose N answers" 
    choose_match = re.search(r'Choose\s+(\d+)\s+answers?', question_text, re.IGNORECASE)
    num_answers = int(choose_match.group(1)) if choose_match else 1
    
    # Clean up question text
    question_text = re.sub(r'\n+', ' ', question_text)
    question_text = re.sub(r'\s+', ' ', question_text)
    question_text = question_text.strip()
    
    if len(question_text) < 15:
        return None
    
    options = {}
    correct_answers = []
    
    for om in option_matches:
        letter = om.group(1).upper()
        opt_text = om.group(2).strip()
        
        # Clean option text
        opt_text = re.sub(r'\n+', ' ', opt_text)
        opt_text = re.sub(r'\s+', ' ', opt_text)
        
        # Check for correct answer markers
        is_correct = False
        if '(Opción marcada' in opt_text:
            is_correct = True
            # But check for "pero incorrecta" - marked but noted as wrong
            if 'pero incorrecta' in opt_text.lower():
                is_correct = False
            opt_text = re.sub(r'\s*\(?\s*Opción marcada[^)]*\)?\s*', '', opt_text).strip()
        
        opt_text = opt_text.strip(' .')
        
        if opt_text and len(opt_text) > 1:
            options[letter] = opt_text
            if is_correct:
                correct_answers.append(letter)
    
    if len(options) < 2:
        return None
    
    return {
        "number": q_num,
        "source": source_name,
        "question": question_text,
        "options": options,
        "correct_answers": sorted(correct_answers),
        "num_expected_answers": num_answers,
    }


def parse_question_block(block, q_num, source_name):
    """Parse a single question block from Sets 1-4 format."""
    
    # Find options: A., B., C., D., E. with possible markers before/after the letter
    # Markers that indicate correct answer: @, ©, (filled dot patterns)
    # Note: Some options have markers like "A.@", "B. ©", "C.(" etc.
    
    # First, let's find all option positions
    # Options can start with: 
    #   A.  or  A.@  or  A.©  or  A.(  or  A oO  or  A. oO  or  A. Oo etc.
    option_pattern = re.compile(
        r'(?:^|\n)\s*([A-Fa-f])\s*[\.\)]\s*(.*?)(?=(?:\n\s*[A-Fa-f]\s*[\.\)])|$)',
        re.DOTALL
    )
    
    option_matches = list(option_pattern.finditer(block))
    
    if len(option_matches) < 2:
        return None
    
    # Question text
    first_opt_start = option_matches[0].start()
    question_text = block[:first_opt_start].strip()
    
    # Clean question text
    question_text = re.sub(r'\n+', ' ', question_text)
    question_text = re.sub(r'\s+', ' ', question_text)
    question_text = question_text.strip()
    
    if len(question_text) < 15:
        return None
    
    # Detect "Choose N answers"
    choose_match = re.search(r'Choose\s+(\d+)\s+answers?', question_text, re.IGNORECASE)
    num_answers = int(choose_match.group(1)) if choose_match else 1
    
    options = {}
    correct_answers = []
    
    for om in option_matches:
        letter = om.group(1).upper()
        raw_text = om.group(2).strip()
        
        # Clean text
        raw_text = re.sub(r'\n+', ' ', raw_text)
        raw_text = re.sub(r'\s+', ' ', raw_text)
        
        # Determine if correct answer based on markers in the raw matched area
        is_correct = False
        
        # Get the full matched string including the letter prefix for marker detection
        full_match_start = om.start()
        prefix_area = block[max(0, full_match_start):full_match_start + 20]
        
        # Correct answer markers in OCR text:
        # @ after letter: "D.@" or "D. @" or "D.@]"
        # © after letter: "B. ©" or "B.©"  
        # Filled circles: "()" with special chars
        # Patterns like "B®" or "c©" or "c.@"
        
        # Check prefix area for markers
        letter_prefix = re.search(rf'{letter}\s*[\.\)]\s*([@©®]|\(\s*@\s*\)|[Gg]@)', prefix_area, re.IGNORECASE)
        if letter_prefix:
            is_correct = True
        
        # Also check for markers right at start of text
        if re.match(r'^[@©®]\s', raw_text):
            is_correct = True
            raw_text = re.sub(r'^[@©®]\s*', '', raw_text)
        
        # Check for various correct-answer patterns
        # "A.@" pattern
        if re.search(rf'{letter}\s*\.\s*[@©®]', prefix_area):
            is_correct = True
        # "A @" pattern  
        if re.search(rf'{letter}\s+[@©®]', prefix_area):
            is_correct = True
        # "(@ " at start of text
        if re.match(r'^\(\s*[@©]\s*\)', raw_text) or re.match(r'^\(@\s', raw_text):
            is_correct = True
            raw_text = re.sub(r'^\(\s*[@©]\s*\)\s*', '', raw_text)
            raw_text = re.sub(r'^\(@\s*', '', raw_text)
        if re.match(r'^@\]?\s', raw_text) or re.match(r'^@$', raw_text):
            is_correct = True
            raw_text = re.sub(r'^@\]?\s*', '', raw_text)
        if re.match(r'^©\s', raw_text):
            is_correct = True
            raw_text = re.sub(r'^©\s*', '', raw_text)
        
        # Clean remaining markers from text
        raw_text = re.sub(r'^\s*[oO©@]\s+[oO©@]\s+', '', raw_text)  # "oO " or "O o" patterns  
        raw_text = re.sub(r'^\s*[oO]\s+[oO]\s+', '', raw_text)
        raw_text = re.sub(r'^\s*[oO©]\s+(?=[A-Z])', '', raw_text)
        raw_text = re.sub(r'^\s*\(\s*\)\s*', '', raw_text)
        raw_text = re.sub(r'^\s*\(\s*[Pp]\s*\)\s*', '', raw_text)
        raw_text = re.sub(r'^\s*[Cc]\s*\)\s*(?=[A-Z])', '', raw_text)
        raw_text = re.sub(r'^\s*[tT]\s*\)\s*(?=[A-Z])', '', raw_text)
        raw_text = re.sub(r'^\s*\[\s*\]\s*', '', raw_text)
        raw_text = re.sub(r'^\s*[Ii]C\s+', '', raw_text)
        raw_text = re.sub(r'^\s*ee\s+', '', raw_text)
        raw_text = re.sub(r'^\s*\(\s*\)\s*', '', raw_text)
        raw_text = re.sub(r'^\s*Cy\s+', '', raw_text)
        raw_text = re.sub(r'^\s*Oo\s+', '', raw_text)
        raw_text = re.sub(r'^\s*oO\s+', '', raw_text)
        raw_text = re.sub(r'^\s*c\)\s+', '', raw_text)
        
        # Remove trailing noise
        raw_text = re.sub(r'\s*[©@]\s*$', '', raw_text)
        raw_text = raw_text.strip()
        
        if raw_text and len(raw_text) > 1:
            options[letter] = raw_text
            if is_correct:
                correct_answers.append(letter)
    
    if len(options) < 2:
        return None
    
    return {
        "number": q_num,
        "source": source_name,
        "question": question_text,
        "options": options,
        "correct_answers": sorted(correct_answers),
        "num_expected_answers": num_answers,
    }


def normalize_for_dedup(text):
    """Normalize text for duplicate detection."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def deduplicate_questions(all_questions):
    """Remove duplicate questions using fuzzy matching."""
    unique = []
    seen_normalized = []
    
    for q in all_questions:
        norm = normalize_for_dedup(q["question"])
        
        is_dup = False
        for i, (existing_norm, existing_q) in enumerate(seen_normalized):
            # Check similarity
            sim = similarity(norm[:100], existing_norm[:100])
            if sim > 0.80:
                is_dup = True
                # Keep the one with more correct answers or more options
                existing = unique[i]
                if (len(q["correct_answers"]) > len(existing["correct_answers"]) or
                    (len(q["correct_answers"]) == len(existing["correct_answers"]) and
                     len(q["options"]) > len(existing["options"]))):
                    unique[i] = q
                    seen_normalized[i] = (norm, q)
                    log(f"  DUP: Replaced Q{existing['number']}({existing['source']}) with Q{q['number']}({q['source']})")
                else:
                    log(f"  DUP: Skipped Q{q['number']}({q['source']}) - dup of Q{existing['number']}({existing['source']})")
                break
        
        if not is_dup:
            unique.append(q)
            seen_normalized.append((norm, q))
    
    return unique


def main():
    all_questions = []
    
    for filename, source_name in SOURCE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        log(f"\n{'='*60}")
        log(f"Processing: {filename} ({source_name})")
        log(f"{'='*60}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Clean the text
        text = clean_text(text)
        
        # Parse based on format
        if source_name == "Estudio":
            questions = parse_estudio_format(text, source_name)
        else:
            questions = parse_sets_format(text, source_name)
        
        log(f"  Questions extracted: {len(questions)}")
        with_answers = sum(1 for q in questions if q['correct_answers'])
        log(f"  With correct answers: {with_answers}")
        
        # Log each question briefly
        for q in questions:
            ans = ','.join(q['correct_answers']) if q['correct_answers'] else '?'
            log(f"    Q{q['number']}: {q['question'][:70]}... [{ans}]")
        
        all_questions.extend(questions)
    
    log(f"\n{'='*60}")
    log(f"TOTAL before dedup: {len(all_questions)}")
    log(f"{'='*60}")
    
    # Deduplicate
    log(f"\nDeduplicating...")
    unique = deduplicate_questions(all_questions)
    log(f"TOTAL after dedup: {len(unique)}")
    
    # Re-number
    for i, q in enumerate(unique, 1):
        q["id"] = i
    
    # Save JSON
    json_path = os.path.join(BASE_DIR, "_extracted_clean.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    log(f"\nJSON: {json_path}")
    
    # Save readable text
    txt_path = os.path.join(BASE_DIR, "_extracted_clean.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        for q in unique:
            f.write(f"{'='*70}\n")
            f.write(f"Q{q['id']} | Source: {q['source']} | Original: #{q['number']}")
            if q['num_expected_answers'] > 1:
                f.write(f" | Choose {q['num_expected_answers']}")
            f.write(f"\n{'='*70}\n")
            f.write(f"{q['question']}\n\n")
            for letter in sorted(q['options'].keys()):
                marker = " ✓" if letter in q['correct_answers'] else ""
                f.write(f"  {letter}. {q['options'][letter]}{marker}\n")
            if q['correct_answers']:
                f.write(f"\n  → Correct: {', '.join(q['correct_answers'])}\n")
            else:
                f.write(f"\n  → Correct: [NOT IDENTIFIED]\n")
            f.write(f"\n")
    log(f"TXT: {txt_path}")
    
    # Summary
    log(f"\n{'='*60}")
    log("SUMMARY:")
    log(f"{'='*60}")
    for _, source_name in SOURCE_FILES:
        count = sum(1 for q in unique if q['source'] == source_name)
        with_ans = sum(1 for q in unique if q['source'] == source_name and q['correct_answers'])
        log(f"  {source_name}: {count} unique questions ({with_ans} with answer)")
    
    no_answer = [q for q in unique if not q['correct_answers']]
    log(f"\nWithout correct answer: {len(no_answer)}")
    for q in no_answer:
        log(f"  - Q{q['id']} ({q['source']} #{q['number']}): {q['question'][:80]}...")
    
    # Write log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    log(f"\nLog: {LOG_FILE}")


if __name__ == "__main__":
    main()
