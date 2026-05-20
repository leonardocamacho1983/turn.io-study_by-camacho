"""Scrape Turn.io public pages to build a company profile."""

from __future__ import annotations

import json
import random
import time
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import REQUEST_TIMEOUT_SECONDS, SCRAPE_DELAY_RANGE_SECONDS, TURNIO_PROFILE_FILE, TURNIO_URLS


def _fetch(url: str, ua: UserAgent) -> BeautifulSoup:
    headers = {"User-Agent": ua.random}
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def _extract_text_list(soup: BeautifulSoup, selector: str, limit: int | None = None) -> List[str]:
    items = [el.get_text(" ", strip=True) for el in soup.select(selector)]
    cleaned = [item for item in items if item]
    if limit:
        return cleaned[:limit]
    return cleaned


def scrape_turnio() -> Dict[str, Any]:
    """Scrape Turn.io homepage, case studies, blog, careers, and pricing pages."""
    ua = UserAgent()

    homepage_url, case_url, blog_url, careers_url, pricing_url = TURNIO_URLS

    data: Dict[str, Any] = {
        "homepage": {},
        "case_studies": {},
        "blog": {},
        "careers": {},
        "pricing": {},
    }

    pages = {
        "homepage": homepage_url,
        "case_studies": case_url,
        "blog": blog_url,
        "careers": careers_url,
        "pricing": pricing_url,
    }

    soups: Dict[str, BeautifulSoup] = {}
    for name, url in pages.items():
        soups[name] = _fetch(url, ua)
        delay = random.uniform(*SCRAPE_DELAY_RANGE_SECONDS)
        time.sleep(delay)

    home = soups["homepage"]
    data["homepage"] = {
        "value_proposition": _extract_text_list(home, "h1, h2", limit=5),
        "taglines": _extract_text_list(home, "p", limit=10),
        "product_features": _extract_text_list(home, "li", limit=20),
    }

    cases = soups["case_studies"]
    data["case_studies"] = {
        "titles": _extract_text_list(cases, "h1, h2, h3"),
        "customer_names": _extract_text_list(cases, "strong, b"),
        "outcomes": _extract_text_list(cases, "p"),
    }

    blog = soups["blog"]
    data["blog"] = {
        "latest_titles": _extract_text_list(blog, "h2, h3", limit=10),
        "latest_summaries": _extract_text_list(blog, "p", limit=10),
    }

    careers = soups["careers"]
    data["careers"] = {
        "open_roles": _extract_text_list(careers, "h2, h3, a"),
        "locations": _extract_text_list(careers, "[class*='location'], [data-location]"),
        "priority_signals": _extract_text_list(careers, "p, li", limit=30),
    }

    pricing = soups["pricing"]
    data["pricing"] = {
        "tiers": _extract_text_list(pricing, "h2, h3"),
        "tier_features": _extract_text_list(pricing, "li"),
        "target_customer_signals": _extract_text_list(pricing, "p", limit=20),
    }

    TURNIO_PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
    TURNIO_PROFILE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data
