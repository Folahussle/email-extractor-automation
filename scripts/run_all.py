from pathlib import Path

from extract_text import extract_from_text_folder
from extract_websites import extract_from_websites
from extract_pdfs import extract_from_pdfs

def main():
    all_emails = set()

    print("=== Extracting from text files ===")
    all_emails |= extract_from_text_folder()

    print("=== Extracting from websites ===")
    all_emails |= extract_from_websites()

    print("=== Extracting from PDFs ===")
    all_emails |= extract_from_pdfs()

    out = Path("output/emails.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(all_emails)), encoding="utf-8")
    print(f"\nTOTAL unique emails: {len(all_emails)}")
    print(f"Combined results saved to {out}")

if __name__ == "__main__":
    main()
