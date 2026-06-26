#!/usr/bin/env python3
"""
Extract questions and answers from Salesforce certification PDFs.
Creates a clean, deduplicated list of all questions.
"""

import pdfplumber
import re
import json
import os

BASE_DIR = r"C:\Users\david\python\cert-salesforce"

PDF_FILES = [
    ("Set 1 (1).pdf", "Set 1"),
    ("Revise 1_Set 2_81.pdf", "Set 2"),
    ("Revise 2_Set 3.pdf", "Set 3"),
    ("Read Second_Set 4_82_.pdf", "Set 4"),
    ("estudio 2026 V2.pdf", "Estudio"),
]


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        print(f"  Pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
    return full_text


def parse_questions_from_text(text, source_name):
    """Parse questions and answers from extracted text."""
    questions = []
    
    # Clean up common OCR artifacts
    text = text.replace('\u2019', "'")
    text = text.replace('\u2018', "'")
    text = text.replace('\u201c', '"')
    text = text.replace('\u201d', '"')
    text = text.replace('\xa0', ' ')
    
    # Pattern to find question numbers like "1 of 64." or "1." at beginning  
    # Also handle patterns like "64. Universal Containers..." from estudio file
    # Try multiple patterns
    
    # Split by question number patterns
    # Pattern 1: "N of 64." style
    # Pattern 2: "N." at start of line style  
    
    # First, try to find all question blocks
    # Look for patterns like "X of 64." or just numbered questions
    q_pattern = re.compile(
        r'(?:^|\n)\s*(\d{1,3})\s*(?:of\s+\d+)?\s*\.\s*'
        r'(.*?)(?=(?:\n\s*\d{1,3}\s*(?:of\s+\d+)?\s*\.)|$)',
        re.DOTALL
    )
    
    matches = list(q_pattern.finditer(text))
    
    if not matches:
        print(f"  WARNING: No questions found with standard pattern in {source_name}")
        return questions
    
    for match in matches:
        q_num = int(match.group(1))
        q_body = match.group(2).strip()
        
        if len(q_body) < 30:
            continue
            
        # Try to extract question text and options
        parsed = parse_question_body(q_body, q_num, source_name)
        if parsed:
            questions.append(parsed)
    
    return questions


def parse_question_body(body, q_num, source_name):
    """Parse a question body into question text and options."""
    
    # Remove common noise
    noise_patterns = [
        r'Mark this item for later review\.?',
        r'©\s*Mark this item.*',
        r'\bHide\b',
        r'Time Remaining:?\s*\d{2}:\d{2}:\d{2}',
        r'Salesforce Certified Identity and Access Management Archite.*?(?=\n)',
        r'Salesforce Certified Identity and Access Management Architect',
        r'kryterion.*?partner.*?\n',
        r'by\s+DRAKE\s+INTERNATIONAL',
        r'by\s+ORAKE\s+INTERNATIONAL',
        r'Fos\s*J\s*next>.*',
        r'Browse.*?submit.*',
        r'@kryterion.*?\n',
        r'previous\s*<\s*next\s*>',
        r'<\s*previous\s*next\s*>',
    ]
    for pattern in noise_patterns:
        body = re.sub(pattern, '', body, flags=re.IGNORECASE)
    
    # Find the options - they typically start with A., B., C., D., E.
    # Options may have various prefixes: "A.", "A.©", "A. ©", "A.@", "A. @", "A. O", etc.
    option_pattern = re.compile(
        r'(?:^|\n)\s*([A-F])\s*[\.\)]\s*[©@O\(]?\s*[©@O\)]?\s*(.*?)(?=(?:\n\s*[A-F]\s*[\.\)]\s*[©@O\(]?)|$)',
        re.DOTALL
    )
    
    option_matches = list(option_pattern.finditer(body))
    
    if len(option_matches) < 2:
        # Try alternative pattern for the estudio format: "- A. text" or "- A. © text"
        option_pattern2 = re.compile(
            r'[-–]\s*([A-F])\s*[\.\)]\s*[©@O\(]?\s*[©@O\)]?\s*(.*?)(?=(?:[-–]\s*[A-F]\s*[\.\)])|$)',
            re.DOTALL
        )
        option_matches = list(option_pattern2.finditer(body))
    
    if len(option_matches) < 2:
        return None
    
    # Question text is everything before the first option
    first_opt_start = option_matches[0].start()
    question_text = body[:first_opt_start].strip()
    
    # Clean up question text
    question_text = re.sub(r'\n+', ' ', question_text)
    question_text = re.sub(r'\s+', ' ', question_text)
    question_text = question_text.strip()
    
    if len(question_text) < 20:
        return None
    
    # Extract "Choose N answers" hint
    choose_match = re.search(r'Choose\s+(\d+)\s+answers?', question_text, re.IGNORECASE)
    num_answers = int(choose_match.group(1)) if choose_match else 1
    
    # Parse options
    options = {}
    correct_answers = []
    
    for opt_match in option_matches:
        letter = opt_match.group(1).upper()
        opt_text = opt_match.group(2).strip()
        
        # Clean option text
        opt_text = re.sub(r'\n+', ' ', opt_text)
        opt_text = re.sub(r'\s+', ' ', opt_text)
        opt_text = opt_text.strip()
        
        # Detect if this is the correct answer
        # Markers: @, ©, (filled circle), bold markers, "(Opción marcada"
        is_correct = False
        raw_prefix = body[opt_match.start():opt_match.start() + 30] if opt_match.start() + 30 < len(body) else body[opt_match.start():]
        
        # Check for markers indicating correct answer
        if re.search(r'[©@]', raw_prefix[:15]):
            is_correct = True
        if '(Opción marcada' in opt_text or 'Opción marcada' in opt_text:
            is_correct = True
            opt_text = re.sub(r'\(?\s*Opción marcada.*?\)?', '', opt_text).strip()
        
        # Remove trailing noise from option text
        opt_text = re.sub(r'\s*©\s*$', '', opt_text)
        opt_text = re.sub(r'\s*@\s*$', '', opt_text)
        
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
        "correct_answers": correct_answers,
        "num_expected_answers": num_answers,
    }


def normalize_question(q_text):
    """Normalize question text for duplicate detection."""
    text = q_text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def deduplicate_questions(all_questions):
    """Remove duplicate questions, keeping the one with the most complete answer."""
    seen = {}
    
    for q in all_questions:
        norm = normalize_question(q["question"])
        
        # Use first 80 chars as a key (enough to identify duplicates)
        key = norm[:80]
        
        if key in seen:
            existing = seen[key]
            # Keep the one with more correct answers identified
            if len(q["correct_answers"]) > len(existing["correct_answers"]):
                seen[key] = q
            elif len(q["options"]) > len(existing["options"]):
                seen[key] = q
        else:
            seen[key] = q
    
    return list(seen.values())


def main():
    all_questions = []
    
    for pdf_name, source_name in PDF_FILES:
        pdf_path = os.path.join(BASE_DIR, pdf_name)
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_name}")
        print(f"{'='*60}")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        
        # Save raw extracted text for reference
        raw_path = os.path.join(BASE_DIR, f"_raw_{source_name.replace(' ', '_')}.txt")
        with open(raw_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  Raw text saved to: {raw_path}")
        
        # Parse questions
        questions = parse_questions_from_text(text, source_name)
        print(f"  Questions found: {len(questions)}")
        
        all_questions.extend(questions)
    
    print(f"\n{'='*60}")
    print(f"TOTAL questions before dedup: {len(all_questions)}")
    
    # Deduplicate
    unique_questions = deduplicate_questions(all_questions)
    print(f"TOTAL questions after dedup: {len(unique_questions)}")
    
    # Re-number
    for i, q in enumerate(unique_questions, 1):
        q["id"] = i
    
    # Save as JSON
    json_path = os.path.join(BASE_DIR, "_extracted_questions.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(unique_questions, f, ensure_ascii=False, indent=2)
    print(f"\nJSON saved to: {json_path}")
    
    # Save as readable text
    txt_path = os.path.join(BASE_DIR, "_extracted_questions.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        for q in unique_questions:
            f.write(f"{'='*60}\n")
            f.write(f"Q{q['id']} (Source: {q['source']}, Original #{q['number']})\n")
            f.write(f"{'='*60}\n")
            f.write(f"{q['question']}\n\n")
            for letter in sorted(q['options'].keys()):
                marker = " ✓" if letter in q['correct_answers'] else ""
                f.write(f"  {letter}. {q['options'][letter]}{marker}\n")
            if q['correct_answers']:
                f.write(f"\n  Correct: {', '.join(q['correct_answers'])}\n")
            else:
                f.write(f"\n  Correct: [not identified]\n")
            f.write(f"\n")
    print(f"Text saved to: {txt_path}")
    
    # Print summary by source
    print(f"\n{'='*60}")
    print("SUMMARY BY SOURCE:")
    for pdf_name, source_name in PDF_FILES:
        count = sum(1 for q in unique_questions if q['source'] == source_name)
        with_answers = sum(1 for q in unique_questions if q['source'] == source_name and q['correct_answers'])
        print(f"  {source_name}: {count} questions ({with_answers} with correct answer identified)")
    
    # Questions without correct answer
    no_answer = [q for q in unique_questions if not q['correct_answers']]
    print(f"\nQuestions without correct answer identified: {len(no_answer)}")
    if no_answer:
        for q in no_answer[:10]:
            print(f"  - Q{q['id']} ({q['source']} #{q['number']}): {q['question'][:80]}...")


if __name__ == "__main__":
    main()
