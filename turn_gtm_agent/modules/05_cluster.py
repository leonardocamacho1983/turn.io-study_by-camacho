"""Market clustering for Turn.io Brazil GTM prioritization."""

from __future__ import annotations

import json
from typing import Any, Dict

from config import BRAZIL_MARKET_FILE, CLUSTERS_FILE, COMPETITIVE_FILE


def build_market_clusters() -> Dict[str, Any]:
    """Build actionable clusters using market and competitive data."""
    # TODO: load and compute from BRAZIL_MARKET_FILE and COMPETITIVE_FILE.
    clusters = {
        "Cluster A": {
            "name": "Large private hospital networks",
            "examples": ["Grupo D'Or", "Hapvida", "NotreDame"],
            "addressable_accounts_estimate": None,
            "deal_size_range": "unknown",
            "sales_cycle_complexity": "high",
            "turnio_fit_score": 4,
            "rationale": "Placeholder rationale.",
            "recommended_entry_approach": "Strategic account-based selling with clinical ops champions.",
        },
        "Cluster B": {
            "name": "Health plan operators",
            "examples": ["ANS-regulated mid-large operators"],
            "addressable_accounts_estimate": None,
            "deal_size_range": "unknown",
            "sales_cycle_complexity": "high",
            "turnio_fit_score": 4,
            "rationale": "Placeholder rationale.",
            "recommended_entry_approach": "Pilot via member engagement and care navigation workflows.",
        },
        "Cluster C": {
            "name": "Healthtech scale-ups",
            "examples": ["Brazil-based Series A+ startups"],
            "addressable_accounts_estimate": None,
            "deal_size_range": "unknown",
            "sales_cycle_complexity": "medium",
            "turnio_fit_score": 5,
            "rationale": "Placeholder rationale.",
            "recommended_entry_approach": "Land via API-first integration and fast time-to-value messaging.",
        },
        "Cluster D": {
            "name": "Public health programmes",
            "examples": ["Federal/state secretariats", "Municipal programs via ImpulsoGov"],
            "addressable_accounts_estimate": None,
            "deal_size_range": "unknown",
            "sales_cycle_complexity": "high",
            "turnio_fit_score": 3,
            "rationale": "Placeholder rationale.",
            "recommended_entry_approach": "Policy-aligned pilot partnerships and grant-backed projects.",
        },
        "Cluster E": {
            "name": "NGOs and impact health organizations",
            "examples": ["Mission-driven health NGOs"],
            "addressable_accounts_estimate": None,
            "deal_size_range": "unknown",
            "sales_cycle_complexity": "medium",
            "turnio_fit_score": 4,
            "rationale": "Placeholder rationale.",
            "recommended_entry_approach": "Template-based program deployments with measurable outcomes.",
        },
    }

    output: Dict[str, Any] = {
        "inputs": {
            "market_data_file": str(BRAZIL_MARKET_FILE),
            "competitive_data_file": str(COMPETITIVE_FILE),
        },
        "clusters": clusters,
        "notes": "Scaffold output. Add data-driven estimation logic.",
    }

    CLUSTERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CLUSTERS_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output
