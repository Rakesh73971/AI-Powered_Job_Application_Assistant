import pdfplumber

async def extract_text_from_pdf(pdf_path: str) -> str:
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
    except Exception as e:
        print(f"[WARNING] PDF extraction failed for {pdf_path}: {e}")
    return extracted_text
