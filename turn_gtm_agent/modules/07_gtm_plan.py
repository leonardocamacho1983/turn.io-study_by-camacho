"""Synthesize all collected data into an executive GTM plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI

from config import DATA_DIR, GTM_JSON_FILE, GTM_MARKDOWN_FILE, OPENAI_API_KEY, OPENAI_MODEL


def _load_json_files(data_dir: Path) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    for file_path in sorted(data_dir.glob("*.json")):
        try:
            payload[file_path.name] = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload[file_path.name] = {"error": "Invalid JSON", "path": str(file_path)}
    return payload


def generate_gtm_plan() -> str:
    """Generate a markdown GTM plan and companion JSON output."""
    dataset = _load_json_files(DATA_DIR)

    fallback_markdown = """# Turn.io Brazil GTM Plan

## 1. Executive Summary
Placeholder summary. Configure OPENAI_API_KEY and rerun for full synthesis.

## 2. Market Opportunity (TAM/SAM/SOM)
Placeholder assumptions.

## 3. Priority Clusters
Placeholder ranking.

## 4. 90-Day Action Plan
Placeholder actions.

## 5. Partner Strategy
Placeholder partner activation plan.

## 6. PR and Thought Leadership Strategy
Placeholder Brazil-specific strategy.

## 7. Year 1 Revenue Model
Placeholder bottom-up model.

## 8. Key Risks and Mitigations
Placeholder risks and mitigations.
"""

    if not OPENAI_API_KEY:
        GTM_MARKDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
        GTM_MARKDOWN_FILE.write_text(fallback_markdown, encoding="utf-8")
        GTM_JSON_FILE.write_text(
            json.dumps({"markdown": fallback_markdown, "inputs": dataset}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return fallback_markdown

    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
    You are a GTM strategist. Using the JSON data below, produce a structured GTM plan in markdown
    with EXACTLY these sections:
    1. Executive Summary (3 paragraphs max)
    2. Market Opportunity (TAM/SAM/SOM with explicit assumptions)
    3. Priority Clusters (ranked, with rationale)
    4. 90-Day Action Plan (specific, named actions, not generic)
    5. Partner Strategy (who to activate first and why)
    6. PR and Thought Leadership Strategy (Brazil-specific)
    7. Year 1 Revenue Model (bottom-up, with assumptions)
    8. Key Risks and Mitigations

    Input data:
    {json.dumps(dataset, ensure_ascii=False)}
    """.strip()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    markdown_output = response.output_text.strip()

    GTM_MARKDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    GTM_MARKDOWN_FILE.write_text(markdown_output, encoding="utf-8")
    GTM_JSON_FILE.write_text(
        json.dumps({"markdown": markdown_output, "inputs": dataset}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return markdown_output
