import re
from pathlib import Path
from PyPDF2 import PdfReader

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_from_pdfs(folder: str = "data/pdfs") -> set[str]:
    base = Path(folder)
    emails: set[str] = set()

    if not base.exists():
        print(f"No pdf folder found at {base}, skipping PDF extraction.")
        return emails

    for pdf_file in base.glob("*.pdf"):
        try:
            reader = PdfReader(str(pdf_file))
            file_emails: set[str] = set()
            for page in reader.pages:
                text = page.extract_text() or ""
                file_emails |= set(re.findall(EMAIL_REGEX, text))
            print(f"{pdf_file} -> {len(file_emails)} emails")
            emails |= file_emails
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")

    return emails

if __name__ == "__main__":
    all_emails = extract_from_pdfs()
    out = Path("output/emails_from_pdfs.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(all_emails)), encoding="utf-8")
    print(f"Saved {len(all_emails)} emails to {out}")
