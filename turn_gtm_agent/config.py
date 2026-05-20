"""Central configuration for the Turn.io Brazil GTM agent."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

CONTEXT_FILE = DATA_DIR / "context.json"
TURNIO_PROFILE_FILE = DATA_DIR / "turnio_profile.json"
BRAZIL_MARKET_FILE = DATA_DIR / "brazil_market.json"
COMPETITIVE_FILE = DATA_DIR / "competitive.json"
CLUSTERS_FILE = DATA_DIR / "clusters.json"
PARTNERS_FILE = DATA_DIR / "partners.json"

GTM_MARKDOWN_FILE = OUTPUTS_DIR / "turn_io_brazil_gtm.md"
GTM_JSON_FILE = OUTPUTS_DIR / "turn_io_brazil_gtm.json"

# OpenAI configuration
OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Turn.io pages
TURNIO_URLS = [
    "https://turn.io",
    "https://turn.io/case-studies",
    "https://turn.io/blog",
    "https://turn.io/careers",
    "https://turn.io/pricing",
]

# Brazil data sources
BRAZIL_DATA_SOURCES = {
    "ANS": "https://dadosabertos.ans.gov.br",
    "DATASUS": "https://datasus.saude.gov.br",
    "IBGE": "https://servicodados.ibge.gov.br/api/v1",
}

# Optional/fallback public source for CFM-like physician figures
CFM_PUBLIC_SOURCE = "https://portal.cfm.org.br"

# Networking behavior
REQUEST_TIMEOUT_SECONDS = 30
SCRAPE_DELAY_RANGE_SECONDS = (1, 3)
