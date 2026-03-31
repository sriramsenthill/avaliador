import re
import requests
from bs4 import BeautifulSoup


def extract_arxiv_id(url: str) -> str:
    """Extract arXiv paper ID from various URL formats."""
    patterns = [
        r"arxiv\.org/abs/([0-9]{4}\.[0-9]+)",
        r"arxiv\.org/pdf/([0-9]{4}\.[0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract arXiv ID from URL: {url}")


def scrape_arxiv_paper(url: str) -> dict:
    """Scrape title and full text from an arXiv abstract page."""
    arxiv_id = extract_arxiv_id(url)
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"

    response = requests.get(abs_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.find("h1", class_="title")
    title = title_tag.get_text(strip=True).replace("Title:", "").strip() if title_tag else "Unknown Title"

    # Extract abstract
    abstract_tag = soup.find("blockquote", class_="abstract")
    abstract = abstract_tag.get_text(strip=True).replace("Abstract:", "").strip() if abstract_tag else ""

    # Try to get full paper text via HTML version
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    full_text = abstract  # fallback

    try:
        html_resp = requests.get(html_url, timeout=20)
        if html_resp.status_code == 200:
            paper_soup = BeautifulSoup(html_resp.text, "html.parser")
            # Remove scripts, styles, nav
            for tag in paper_soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            full_text = paper_soup.get_text(separator="\n", strip=True)
    except Exception:
        pass  # Fall back to abstract only

    # Truncate to ~12k tokens worth of characters (~48k chars) to stay safe
    MAX_CHARS = 40000
    if len(full_text) > MAX_CHARS:
        full_text = full_text[:MAX_CHARS] + "\n\n[... truncated for token limit ...]"

    return {"title": title, "raw_text": full_text, "abstract": abstract}