"""Competitive landscape mapping for Brazil digital health players."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from config import COMPETITIVE_FILE


COMPETITORS = [
    "Zenvia",
    "Conexa Saúde",
    "Docway",
    "Nilo Saúde",
    "Sami Saúde",
    "Pipo Saúde",
    "Qualisaude",
    "Beneva",
]


def map_competitors() -> Dict[str, Any]:
    """Map competitors with public, web-derived positioning signals."""
    records: List[Dict[str, Any]] = []

    for name in COMPETITORS:
        records.append(
            {
                "name": name,
                "business_model": "unknown",
                "target_segment": "unknown",
                "funding_status": "unknown",
                "product_focus": "unknown",
                "weaknesses_vs_turnio": [],
                "notes": "Placeholder record. Add web search and scraping adapters.",
            }
        )

    extra = {
        "name": "WhatsApp-native health communication platform (to identify)",
        "business_model": "unknown",
        "target_segment": "unknown",
        "funding_status": "unknown",
        "product_focus": "unknown",
        "weaknesses_vs_turnio": [],
        "notes": "Placeholder for additional identified market player.",
    }
    records.append(extra)

    output = {
        "competitors": records,
        "method": "Scaffold output; implement web search, scrape, and synthesis pipeline.",
    }

    COMPETITIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COMPETITIVE_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output
