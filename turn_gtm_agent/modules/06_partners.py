"""Partner ecosystem mapping for Turn.io Brazil market entry."""

from __future__ import annotations

import json
from typing import Any, Dict

from config import PARTNERS_FILE


def map_partner_ecosystem() -> Dict[str, Any]:
    """Identify candidate partners and suggested activation models."""
    output: Dict[str, Any] = {
        "system_integrators": {
            "organizations": [],
            "partnership_model": "co-sell/integration",
            "estimated_revenue_potential": "unknown",
            "activation_effort": "high",
        },
        "whatsapp_bsps": {
            "organizations": [],
            "partnership_model": "integration/referral",
            "estimated_revenue_potential": "unknown",
            "activation_effort": "medium",
        },
        "health_it_consultancies": {
            "organizations": [],
            "partnership_model": "referral/reseller",
            "estimated_revenue_potential": "unknown",
            "activation_effort": "medium",
        },
        "digital_health_accelerators": {
            "organizations": [],
            "partnership_model": "referral/innovation programs",
            "estimated_revenue_potential": "unknown",
            "activation_effort": "low",
        },
        "academic_institutions": {
            "organizations": [],
            "partnership_model": "research/co-development",
            "estimated_revenue_potential": "unknown",
            "activation_effort": "medium",
        },
        "notes": "Scaffold output. Populate with 3-5 named orgs per category.",
    }

    PARTNERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PARTNERS_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    return output
