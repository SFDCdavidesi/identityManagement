#!/usr/bin/env python3
"""
Robust Q&A extraction from Salesforce Identity exam files.
Strategy: Find question blocks by detecting option groups (A/B/C/D patterns),
then extract the question text before each option group.
Does NOT rely on cleanly-parsed question numbers.
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

log_lines = []
def log(msg):
    log_lines.append(msg)


def preprocess_text(text, source):
    """Clean common OCR noise from text."""
    # Remove page markers
    text = re.sub(r'---\s*PÁGINA\s*\d+\s*---', '\n', text)
    # Remove exam headers
    text = re.sub(r'Salesforce Certified Identity and Access Management Archite[^\n]*', '\n', text)
    text = re.sub(r'Salesrorce Certiried Laentity[^\n]*', '\n', text)
    text = re.sub(r'Serssiviee Verse[^\n]*', '\n', text)
    text = re.sub(r'Sesser ee Corse[^\n]*', '\n', text)
    text = re.sub(r'DaIESIUICE CETUNeU LUENULy[^\n]*', '\n', text)
    text = re.sub(r'Time Remaining[^\n]*', '\n', text)
    text = re.sub(r'Time Rem[:\s]*\n', '\n', text)
    text = re.sub(r'kryterion[^\n]*', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'by\s+[DO]RAKE\s+INTERNATIONAL[^\n]*', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'[©O]?\s*Mark this item for later review\.?', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'[©O]?\s*Merk this item for later review\.?', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'@kryterion[^\n]*', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'Translation Value:.*?responses\.?', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'M\s+Mark this item[^\n]*', '\n', text)
    text = re.sub(r'[ACFT7]\)?\s*Mark this item[^\n]*', '\n', text)
    text = re.sub(r'TF\)\s*Mark this item[^\n]*', '\n', text)
    text = re.sub(r'Press the "Pr[n]t Scrn"[^\n]*', '\n', text)
    
    # Remove isolated noise words
    for noise in [r'\{?\s*snow\s*\}?', r'\{?\s*Hide\s*\}?', r'\{?\s*show\s*\}?',
                  r'\{?\s*stow\s*\}?', r'\bFos\s*J\s*next>[^\n]*', r'previous[^\n]*next[^\n]*',
                  r'Browse[^\n]*submit', r'€ED', r'[Ss]r\)', r'\bEES\b', r'\bBasa\b',
                  r'=a\s*ae\s*Eas', r'=a\b', r'Re\s+GS\s+SSE\s+SSS',
                  r'Ss\s+(?:sr|On|oo|a)\s*\)', r'eg\s+Ss\s+ed\)',
                  r'ry\s+ree', r'[Ss]ho\b', r'\b[Gg][pr]\b', r'\b@rr?\b', r'\b@rh\b',
                  r'\bSO\b\s*\n']:
        text = re.sub(noise, '', text, flags=re.IGNORECASE)
    
    # OCR char fixes
    text = text.replace('€.', 'C.')
    text = text.replace('¢.', 'C.')
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\xa0', ' ')
    
    # For estudio file, compress double-spaced characters
    if source == "Estudio":
        lines = text.split('\n')
        cleaned = []
        for line in lines:
            if re.match(r'^[\s]*[A-Za-z]\s{2,}[A-Za-z]\s{2,}', line):
                line = re.sub(r'(?<=\S)\s{2,}(?=\S)', ' ', line)
            cleaned.append(line)
        text = '\n'.join(cleaned)
    
    return text


def find_option_groups(text):
    """Find groups of options (A, B, C, D, E) in the text.
    Returns list of (start_of_first_option, list_of_option_matches) tuples.
    """
    # Find all option-like patterns
    # Match: letter followed by . or ) at start of line or after whitespace
    # Options are typically: A., B., C., D., E., sometimes with markers
    
    all_options = []
    
    # Pattern for options in sets format: "A." or "A.©" or "A.@" etc at start of line
    if True:
        pattern = re.compile(
            r'(?:^|\n)\s*'  # start of line
            r'([A-Ea-e])\s*[\.\)]'  # letter + dot/paren
            r'\s*'
            r'([^\n]*(?:\n(?!\s*[A-Ea-e]\s*[\.\)])[^\n]*)*)',  # option text (multi-line until next option)
            re.MULTILINE
        )
        
        for m in pattern.finditer(text):
            letter = m.group(1).upper()
            opt_start = m.start()
            opt_text = m.group(2).strip()
            all_options.append({
                'letter': letter,
                'start': opt_start,
                'end': m.end(),
                'raw': m.group(0),
                'text': opt_text,
            })
    
    # Group consecutive options into question option sets
    groups = []
    current_group = []
    seen_letters = set()
    
    for opt in all_options:
        letter = opt['letter']
        
        # Check if this starts a new group
        if letter in seen_letters:
            # We've seen this letter before - save current group and start new
            if len(current_group) >= 2:
                groups.append(current_group)
            current_group = [opt]
            seen_letters = {letter}
        elif letter == 'A' and current_group:
            # 'A' always starts a new group (unless it's the first option)
            if len(current_group) >= 2:
                groups.append(current_group)
            current_group = [opt]
            seen_letters = {letter}
        else:
            # Check for reasonable sequence
            if current_group:
                last_letter = current_group[-1]['letter']
                expected = chr(ord(last_letter) + 1)
                # Allow some gaps (OCR might miss a letter)
                gap = ord(letter) - ord(last_letter)
                if 0 < gap <= 2:
                    current_group.append(opt)
                    seen_letters.add(letter)
                else:
                    # Too big a gap or backwards - new group
                    if len(current_group) >= 2:
                        groups.append(current_group)
                    current_group = [opt]
                    seen_letters = {letter}
            else:
                current_group = [opt]
                seen_letters = {letter}
    
    # Don't forget the last group
    if len(current_group) >= 2:
        groups.append(current_group)
    
    return groups


def find_option_groups_estudio(text):
    """Find option groups in the estudio format with "- A." pattern."""
    pattern = re.compile(
        r'[-–]\s+([A-Ea-e])\.\s+(.*?)(?=\s*[-–]\s+[A-Ea-e]\.\s|$)',
        re.DOTALL
    )
    
    all_options = list(pattern.finditer(text))
    
    groups = []
    current_group = []
    seen_letters = set()
    
    for m in all_options:
        letter = m.group(1).upper()
        opt = {
            'letter': letter,
            'start': m.start(),
            'end': m.end(),
            'raw': m.group(0),
            'text': m.group(2).strip(),
        }
        
        if letter in seen_letters or (letter == 'A' and current_group):
            if len(current_group) >= 2:
                groups.append(current_group)
            current_group = [opt]
            seen_letters = {letter}
        else:
            current_group.append(opt)
            seen_letters.add(letter)
    
    if len(current_group) >= 2:
        groups.append(current_group)
    
    return groups


def extract_question_text(text, group_start, prev_group_end):
    """Extract question text from the region before the options."""
    # Look backwards from the first option to find the question text
    region = text[prev_group_end:group_start].strip()
    
    # Remove leading noise
    region = re.sub(r'^\s*\d{1,2}\s*(of\s+64\s*)?\.?\s*', '', region)
    region = re.sub(r'^[^\w]*(?:eo|Bor|Dor|Dot|Bot|Cy|Mot|Gor|Py|LU\])\s*(of\s+)?64\s*\.?\s*', '', region, flags=re.IGNORECASE)
    region = re.sub(r'^[^\w]*(?:@|§B|eS|\(|[Gg]|Me)\s*(of\s+|or\s+)?64\s*\.?\s*', '', region, flags=re.IGNORECASE)
    
    # Remove category headers from estudio
    for cat in ['Identity Management Concepts', 'Community \\(Partner and Customer\\)',
                'Accepting Third-Party Identity in Salesforce', 'Salesforce as an Identity Provider',
                'Salesforce Identity', 'OAuth']:
        region = re.sub(rf'^\s*{cat}\s*\n?', '', region)
    
    # Clean whitespace
    region = re.sub(r'\n+', ' ', region)
    region = re.sub(r'\s+', ' ', region)
    region = region.strip()
    
    # If the question text is too short, it might be just noise
    if len(region) < 20:
        return None
    
    return region


def detect_correct_answers(opt, source):
    """Detect if an option is marked as correct."""
    letter = opt['letter']
    raw = opt['raw']
    text = opt['text']
    
    is_correct = False
    
    if source == "Estudio":
        if 'Opción marcada' in text:
            is_correct = True
            if 'pero incorrecta' in text.lower():
                is_correct = False
    else:
        # Look for markers in the raw text near the letter
        # Patterns: "D.@", "D. @", "B.©", "c©", "c.@", "@@ text", "@ text"
        prefix_pattern = rf'{letter}\s*[\.\)]\s*[@©®]'
        if re.search(prefix_pattern, raw[:20], re.IGNORECASE):
            is_correct = True
        
        # Check start of text for markers
        if re.match(r'^[@©®]\s', text):
            is_correct = True
        if re.match(r'^\(\s*[@©]\s*\)', text):
            is_correct = True
        if re.match(r'^@@\s', text):
            is_correct = True
        
        # Check the raw match for @@ or @ right after the letter.
        raw_start = raw[:30]
        if re.search(rf'{letter}\s*[\.\)]\s*@@', raw_start, re.IGNORECASE):
            is_correct = True
        if re.search(rf'{letter}\s*[\.\)]\s*@\s+[A-Z]', raw_start, re.IGNORECASE):
            is_correct = True
        
        # Pattern: "D.@" where @ is right after dot (no space sometimes: "D.@")
        if re.search(rf'{letter}\.@', raw_start):
            is_correct = True
        
        # Special: text starts with "(P" or "(@" or similar OCR markers for filled circles  
        if re.match(r'^\(\s*[@PpB]\s*\)', text):
            is_correct = True

        # For Set 3: Some options have special markers like "5@", "x)", "EX)"
        if re.match(r'^[xX5s]\)', text[:5]):
            is_correct = True
    
    return is_correct


def clean_option_text(text, source):
    """Clean option text of markers and noise."""
    if source == "Estudio":
        text = re.sub(r'\s*\(?\s*Opción marcada[^)]*\)?\s*', '', text)
    
    # Remove leading markers
    text = re.sub(r'^[@©®]\s*', '', text)
    text = re.sub(r'^@@\s*', '', text)
    text = re.sub(r'^\(\s*[@©PpB]\s*\)\s*', '', text)
    text = re.sub(r'^\(\s*\)\s*', '', text)
    text = re.sub(r'^[oO©]\s+[oO©]\s+', '', text)
    text = re.sub(r'^[oO]\s+[oO]\s+', '', text)
    text = re.sub(r'^[oO©]\s+(?=[A-Z])', '', text)
    text = re.sub(r'^Oo\s+', '', text)
    text = re.sub(r'^oO\s+', '', text)
    text = re.sub(r'^Cy\s+', '', text)
    text = re.sub(r'^[iI]C\s+', '', text)
    text = re.sub(r'^ee\s+', '', text)
    text = re.sub(r'^c\)\s+', '', text)
    text = re.sub(r'^t\)\s+', '', text)
    text = re.sub(r'^[xX5s]\)\s*', '', text)
    text = re.sub(r'^EX\)\s*', '', text)
    
    # Remove trailing markers/noise
    text = re.sub(r'\s*[@©]\s*$', '', text)
    text = re.sub(r'\s*ing:\s*\d{2}:\d{2}:\d{2}\s*$', '', text)
    
    # Clean whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip(' .')
    
    return text


def extract_questions_from_file(filepath, source_name):
    """Extract all questions from a source file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = preprocess_text(text, source_name)
    
    # Find option groups
    if source_name == "Estudio":
        groups = find_option_groups_estudio(text)
    else:
        groups = find_option_groups(text)
    
    log(f"  Option groups found: {len(groups)}")
    
    questions = []
    prev_end = 0
    
    for gi, group in enumerate(groups):
        first_opt_start = group[0]['start']
        
        # Extract question text
        q_text = extract_question_text(text, first_opt_start, prev_end)
        
        prev_end = group[-1]['end']
        
        if not q_text:
            log(f"    Group {gi+1}: No question text found")
            continue
        
        # Detect "Choose N answers"
        choose_match = re.search(r'Choose\s+(\d+)\s+answers?', q_text, re.IGNORECASE)
        num_answers = int(choose_match.group(1)) if choose_match else 1
        
        # Parse options
        options = {}
        correct_answers = []
        
        for opt in group:
            letter = opt['letter']
            is_correct = detect_correct_answers(opt, source_name)
            clean_text_val = clean_option_text(opt['text'], source_name)
            
            if clean_text_val and len(clean_text_val) > 1:
                options[letter] = clean_text_val
                if is_correct:
                    correct_answers.append(letter)
        
        if len(options) < 2:
            log(f"    Group {gi+1}: Too few options ({len(options)})")
            continue
        
        questions.append({
            "source": source_name,
            "question": q_text,
            "options": options,
            "correct_answers": sorted(list(set(correct_answers))),
            "num_expected_answers": num_answers,
        })
    
    return questions


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
    dup_count = 0
    
    for q in all_questions:
        norm = normalize_for_dedup(q["question"])
        # Use first ~100 chars for matching
        key = norm[:100]
        
        is_dup = False
        for i, (existing_key, existing_q) in enumerate(seen_normalized):
            sim = similarity(key, existing_key)
            if sim > 0.75:
                is_dup = True
                dup_count += 1
                # Keep the one with more correct answers or more options
                existing = unique[i]
                score_new = len(q["correct_answers"]) * 10 + len(q["options"]) + len(q["question"])
                score_exist = len(existing["correct_answers"]) * 10 + len(existing["options"]) + len(existing["question"])
                if score_new > score_exist:
                    unique[i] = q
                    seen_normalized[i] = (normalize_for_dedup(q["question"])[:100], q)
                break
        
        if not is_dup:
            unique.append(q)
            seen_normalized.append((key, q))
    
    log(f"  Duplicates removed: {dup_count}")
    return unique


def main():
    all_questions = []
    
    for filename, source_name in SOURCE_FILES:
        filepath = os.path.join(BASE_DIR, filename)
        log(f"\n{'='*60}")
        log(f"Processing: {filename}")
        log(f"{'='*60}")
        
        questions = extract_questions_from_file(filepath, source_name)
        
        log(f"  Questions extracted: {len(questions)}")
        with_answers = sum(1 for q in questions if q['correct_answers'])
        log(f"  With correct answers: {with_answers}")
        
        all_questions.extend(questions)
    
    log(f"\n{'='*60}")
    log(f"TOTAL before dedup: {len(all_questions)}")
    log(f"{'='*60}")
    
    # Deduplicate
    log(f"\nDeduplicating...")
    unique = deduplicate_questions(all_questions)
    log(f"TOTAL after dedup: {len(unique)}")
    
    # Assign IDs
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
            f.write(f"Q{q['id']} | Source: {q['source']}")
            if q['num_expected_answers'] > 1:
                f.write(f" | Choose {q['num_expected_answers']}")
            f.write(f"\n{'='*70}\n")
            f.write(f"{q['question']}\n\n")
            for letter in sorted(q['options'].keys()):
                marker = " [CORRECT]" if letter in q['correct_answers'] else ""
                f.write(f"  {letter}. {q['options'][letter]}{marker}\n")
            if q['correct_answers']:
                f.write(f"\n  Correct: {', '.join(q['correct_answers'])}\n")
            else:
                f.write(f"\n  Correct: [NOT IDENTIFIED]\n")
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
        log(f"  - Q{q['id']} ({q['source']}): {q['question'][:80]}...")
    
    # Write log
    log_path = os.path.join(BASE_DIR, "_extraction_v3_log.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    
    # Print summary to stdout
    print(f"Extracted: {len(all_questions)} total, {len(unique)} unique after dedup")
    print(f"With correct answer: {sum(1 for q in unique if q['correct_answers'])}")
    print(f"Without correct answer: {len(no_answer)}")
    for _, source_name in SOURCE_FILES:
        count = sum(1 for q in unique if q['source'] == source_name)
        with_ans = sum(1 for q in unique if q['source'] == source_name and q['correct_answers'])
        print(f"  {source_name}: {count} unique ({with_ans} with answer)")


if __name__ == "__main__":
    main()
