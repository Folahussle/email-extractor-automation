import re
from pathlib import Path

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_from_text_folder(folder: str = "data/text") -> set[str]:
    base = Path(folder)
    emails: set[str] = set()

    if not base.exists():
        print(f"No text folder found at {base}, skipping text extraction.")
        return emails

    for txt_file in base.glob("*.txt"):
        try:
            text = txt_file.read_text(encoding="utf-8", errors="ignore")
            found = set(re.findall(EMAIL_REGEX, text))
            print(f"{txt_file} -> {len(found)} emails")
            emails |= found
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")

    return emails

if __name__ == "__main__":
    all_emails = extract_from_text_folder()
    out = Path("output/emails_from_text.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(all_emails)), encoding="utf-8")
    print(f"Saved {len(all_emails)} emails to {out}")
