# extract_text.py
import os
from pathlib import Path

PDF_PATH = "msu_textbook.pdf"   # change if your file has different name/path
OUT_TXT = "msu_textbook.txt"
# If you installed tesseract and it's not on PATH, set its path here, e.g. r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_CMD = None  

def try_imports():
    try:
        import pdfplumber
    except Exception as e:
        raise SystemExit("Missing dependency: pdfplumber. Install with: pip install pdfplumber")
    try:
        from pdf2image import convert_from_path
        pdf2image_ok = True
    except Exception:
        pdf2image_ok = False
    try:
        import pytesseract
        pytesseract_ok = True
    except Exception:
        pytesseract_ok = False
    return pdfplumber, pdf2image_ok, pytesseract_ok

def extract_text(pdf_path):
    pdfplumber, pdf2image_ok, pytesseract_ok = try_imports()
    text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"Opened PDF: {total} pages")
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""

            if len(page_text.strip()) > 50:
                text_pages.append(page_text)
            else:

                if pdf2image_ok and pytesseract_ok:
                    try:
                        from pdf2image import convert_from_path
                        import pytesseract
                        images = convert_from_path(pdf_path, first_page=i, last_page=i, dpi=300)
                        if images:
                            ocr_text = pytesseract.image_to_string(images[0])
                            text_pages.append(ocr_text)
                            print(f"OCR used for page {i}")
                        else:
                            text_pages.append("")
                            print(f"No image for OCR on page {i}")
                    except Exception as e:
                        print(f"OCR error on page {i}: {e}")
                        text_pages.append(page_text)
                else:
            
                    text_pages.append(page_text)
                    if not page_text.strip():
                        print(f"Page {i} had no selectable text and OCR not available.")
    return "\n\n".join(text_pages)

def main():
    p = Path(PDF_PATH)
    if not p.exists():
        print(f"PDF not found at {PDF_PATH}. Put your textbook there or change PDF_PATH in the script.")
        return

    if TESSERACT_CMD:
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        except Exception:
            pass
    print("Starting extraction (this may take a bit)...")
    full_text = extract_text(PDF_PATH)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Saved text to {OUT_TXT}")
    print(f"Total characters extracted: {len(full_text)}")
    sample = full_text[:2000].replace("\n", " ")
    print("\n--- SAMPLE (first ~2000 chars) ---\n")
    print(sample)
    print("\n--- END SAMPLE ---\n")

if __name__ == "__main__":
    main()
