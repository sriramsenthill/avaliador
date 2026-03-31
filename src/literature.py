from __future__ import annotations

import re
from html import unescape
from typing import Iterable
from urllib.parse import quote_plus
from xml.etree import ElementTree

import requests


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "into", "is", "it", "its", "of", "on", "or", "that", "the", "their",
    "this", "to", "toward", "using", "via", "with",
}


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().lower()


def _title_similarity(a: str, b: str) -> float:
    a_tokens = set(re.findall(r"[a-z0-9]+", a.lower()))
    b_tokens = set(re.findall(r"[a-z0-9]+", b.lower()))
    if not a_tokens or not b_tokens:
        return 0.0
    overlap = len(a_tokens & b_tokens)
    return overlap / max(len(a_tokens), len(b_tokens))


def _build_queries(title: str, abstract: str) -> list[str]:
    title_tokens = [
        token for token in re.findall(r"[A-Za-z0-9]+", title)
        if len(token) > 3 and token.lower() not in STOPWORDS
    ]
    abstract_tokens = [
        token for token in re.findall(r"[A-Za-z0-9]+", abstract)
        if len(token) > 5 and token.lower() not in STOPWORDS
    ]

    keyword_query = " AND ".join(f'all:"{token}"' for token in title_tokens[:4])
    backup_query = " AND ".join(f'all:"{token}"' for token in abstract_tokens[:3])

    queries = [f'ti:"{title}"']
    if keyword_query:
        queries.append(keyword_query)
    if backup_query:
        queries.append(backup_query)
    return queries


def _text(elem: ElementTree.Element | None, default: str = "") -> str:
    if elem is None or elem.text is None:
        return default
    return unescape(re.sub(r"\s+", " ", elem.text).strip())


def _parse_entry(entry: ElementTree.Element) -> dict:
    authors = [
        _text(author.find("atom:name", ATOM_NS))
        for author in entry.findall("atom:author", ATOM_NS)
    ]
    summary = _text(entry.find("atom:summary", ATOM_NS))
    return {
        "title": _text(entry.find("atom:title", ATOM_NS)),
        "summary": summary[:420] + ("..." if len(summary) > 420 else ""),
        "published": _text(entry.find("atom:published", ATOM_NS))[:10],
        "url": _text(entry.find("atom:id", ATOM_NS)),
        "authors": ", ".join(author for author in authors[:4] if author),
    }


def _fetch_query(query: str, max_results: int) -> list[dict]:
    url = (
        f"{ARXIV_API_URL}?search_query={quote_plus(query)}"
        f"&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    )
    response = requests.get(url, timeout=20, headers={"User-Agent": "avaliador/1.0"})
    response.raise_for_status()
    root = ElementTree.fromstring(response.text)
    return [_parse_entry(entry) for entry in root.findall("atom:entry", ATOM_NS)]


def _dedupe_by_title(entries: Iterable[dict], seed_title: str) -> list[dict]:
    seen = {_normalize_title(seed_title)}
    deduped = []
    for entry in entries:
        normalized = _normalize_title(entry.get("title", ""))
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(entry)
    return deduped


def search_related_work(title: str, abstract: str, limit: int = 5) -> list[dict]:
    candidates: list[dict] = []
    for query in _build_queries(title, abstract):
        try:
            candidates.extend(_fetch_query(query, max_results=limit))
        except Exception:
            continue

    deduped = _dedupe_by_title(candidates, seed_title=title)
    ranked = sorted(
        deduped,
        key=lambda item: _title_similarity(title, item.get("title", "")),
        reverse=True,
    )
    return ranked[:limit]
