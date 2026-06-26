import pdfplumber, sys, os
BASE = r"C:\Users\david\python\cert-salesforce"
log = open(os.path.join(BASE, "_test_log.txt"), "w", encoding="utf-8")
log.write("Starting...\n")
try:
    for name in ["Set 1 (1).pdf", "Revise 1_Set 2_81.pdf", "Revise 2_Set 3.pdf", "Read Second_Set 4_82_.pdf", "estudio 2026 V2.pdf"]:
        path = os.path.join(BASE, name)
        pdf = pdfplumber.open(path)
        log.write(f"{name}: {len(pdf.pages)} pages\n")
        # Extract first page text preview
        t = pdf.pages[0].extract_text()
        if t:
            log.write(f"  First 200 chars: {t[:200]}\n")
        else:
            log.write("  No text extracted from page 0\n")
        pdf.close()
    log.write("DONE\n")
except Exception as e:
    log.write(f"ERROR: {e}\n")
log.close()
