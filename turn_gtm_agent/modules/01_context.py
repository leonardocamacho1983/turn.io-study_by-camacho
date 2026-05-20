"""Context extraction module from call transcripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI

from config import CONTEXT_FILE, OPENAI_API_KEY, OPENAI_MODEL


def load_call_transcript(filepath: str) -> Dict[str, Any]:
    """Load a transcript and extract structured GTM context using OpenAI.

    Args:
        filepath: Path to a plain-text transcript file.

    Returns:
        Structured dictionary with company and market signals.
    """
    transcript_path = Path(filepath)
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    raw_text = transcript_path.read_text(encoding="utf-8")

    # Placeholder fallback structure in case API key is not configured.
    fallback = {
        "company_signals": [],
        "market_signals": [],
        "pain_points": [],
        "opportunities": [],
        "key_names": [],
        "notes": "OPENAI_API_KEY missing; generated placeholder output.",
    }

    if not OPENAI_API_KEY:
        CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONTEXT_FILE.write_text(json.dumps(fallback, indent=2, ensure_ascii=False), encoding="utf-8")
        return fallback

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    Extract structured insights from this Turn.io call transcript.
    Return STRICT JSON with keys:
    company_signals, market_signals, pain_points, opportunities, key_names.

    Transcript:
    {raw_text}
    """.strip()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.output_text.strip()
    parsed = json.loads(content)

    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONTEXT_FILE.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    return parsed
