import json
import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Only crawl official Carleton domains (public)
ALLOWED_DOMAINS = {
    "carleton.ca",
    "www.carleton.ca",
    "admissions.carleton.ca",
    "calendar.carleton.ca",
    "library.carleton.ca",
    "events.carleton.ca",
    "graduate.carleton.ca",
    "athletics.carleton.ca",
    "goravens.ca",
}

USER_AGENT = "CampusAssistBot/0.1 (student project)"
TIMEOUT = 15
SLEEP_SECONDS = 0.4

# Skip these file types (not HTML pages)
SKIP_EXTENSIONS = re.compile(r"\.(pdf|jpg|jpeg|png|gif|zip|mp4|mp3|docx?)$", re.IGNORECASE)

def is_allowed_url(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False

        host = (p.netloc or "").lower()
        if host not in ALLOWED_DOMAINS:
            return False

        if SKIP_EXTENSIONS.search(p.path):
            return False

        return True
    except Exception:
        return False

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Remove stuff that creates noise
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_links(base_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    urls = []
    for a in soup.select("a[href]"):
        href = (a.get("href") or "").strip()
        if not href:
            continue
        u = urljoin(base_url, href).split("#", 1)[0]  # remove fragment
        urls.append(u)
    return urls

def crawl(seed_urls: list[str], max_pages: int = 300) -> None:
    seen = set()
    q = deque(seed_urls)

    headers = {"User-Agent": USER_AGENT}
    out_path = "data/raw_pages.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        while q and len(seen) < max_pages:
            url = q.popleft()

            if url in seen:
                continue
            if not is_allowed_url(url):
                continue

            try:
                r = requests.get(url, headers=headers, timeout=TIMEOUT)

                if r.status_code != 200:
                    seen.add(url)
                    continue

                ctype = r.headers.get("Content-Type", "")
                if "text/html" not in ctype:
                    seen.add(url)
                    continue

                text = extract_text(r.text)

                # Skip tiny pages (usually empty/redirect/utility pages)
                if len(text) < 300:
                    seen.add(url)
                    continue

                f.write(json.dumps({"url": url, "text": text}, ensure_ascii=False) + "\n")
                f.flush()

                # Add new links to queue
                for link in extract_links(url, r.text):
                    if link not in seen and is_allowed_url(link):
                        q.append(link)

                seen.add(url)
                print(f"[{len(seen)}/{max_pages}] saved: {url}")

                time.sleep(SLEEP_SECONDS)

            except Exception as e:
                print(f"error: {url} -> {e}")
                seen.add(url)

if __name__ == "__main__":
    # Start small. You can add more seed pages later.
    seeds = [
        "https://carleton.ca/",
        "https://carleton.ca/campus/map/",
        "https://carleton.ca/registrar/",
        "https://carleton.ca/studentaffairs/",
        "https://carleton.ca/its/",
        "https://calendar.carleton.ca/",
        "https://admissions.carleton.ca/",
        "https://library.carleton.ca/",
    ]

    crawl(seeds, max_pages=300)