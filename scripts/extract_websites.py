import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_from_websites(urls_file: str = "data/urls.txt") -> set[str]:
    path = Path(urls_file)
    emails: set[str] = set()

    if not path.exists():
        print(f"No urls.txt found at {path}, skipping website extraction.")
        return emails

    urls = [u.strip() for u in path.read_text().splitlines() if u.strip()]
    if not urls:
        print("urls.txt is empty, skipping website extraction.")
        return emails

    def fetch(url: str) -> set[str]:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(" ", strip=True)
            found = set(re.findall(EMAIL_REGEX, text))
            print(f"{url} -> {len(found)} emails")
            return found
        except Exception as e:
            print(f"Error with {url}: {e}")
            return set()

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch, url): url for url in urls}
        for fut in as_completed(futures):
            emails |= fut.result()

    return emails

if __name__ == "__main__":
    all_emails = extract_from_websites()
    out = Path("output/emails_from_websites.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(all_emails)), encoding="utf-8")
    print(f"Saved {len(all_emails)} emails to {out}")
