"""CLI orchestrator for Turn.io Brazil GTM agent."""

from __future__ import annotations

import argparse
import importlib.util
import json
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from config import (
    BRAZIL_MARKET_FILE,
    CLUSTERS_FILE,
    COMPETITIVE_FILE,
    CONTEXT_FILE,
    DATA_DIR,
    GTM_JSON_FILE,
    GTM_MARKDOWN_FILE,
    PARTNERS_FILE,
    TURNIO_PROFILE_FILE,
)

console = Console()


ModuleFn = Callable[[], Any]


def _load_module_function(module_file: str, fn_name: str) -> ModuleFn:
    base_dir = Path(__file__).resolve().parent
    path = base_dir / "modules" / module_file
    spec = importlib.util.spec_from_file_location(module_file.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fn = getattr(module, fn_name)
    return fn


def _safe_load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def run_pipeline(skip_scrape: bool, single_module: str | None) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    modules: List[Dict[str, Any]] = [
        {"id": "01", "file": "01_context.py", "fn": "load_call_transcript", "args": ["data/transcript.txt"], "output": CONTEXT_FILE},
        {"id": "02", "file": "02_scrape_turnio.py", "fn": "scrape_turnio", "args": [], "output": TURNIO_PROFILE_FILE},
        {"id": "03", "file": "03_market_data.py", "fn": "fetch_brazil_health_market", "args": [], "output": BRAZIL_MARKET_FILE},
        {"id": "04", "file": "04_competitive.py", "fn": "map_competitors", "args": [], "output": COMPETITIVE_FILE},
        {"id": "05", "file": "05_cluster.py", "fn": "build_market_clusters", "args": [], "output": CLUSTERS_FILE},
        {"id": "06", "file": "06_partners.py", "fn": "map_partner_ecosystem", "args": [], "output": PARTNERS_FILE},
        {"id": "07", "file": "07_gtm_plan.py", "fn": "generate_gtm_plan", "args": [], "output": GTM_MARKDOWN_FILE},
    ]

    if single_module:
        modules = [m for m in modules if m["id"] == single_module]
        if not modules:
            raise ValueError(f"Unknown module id: {single_module}")

    results = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        for mod in modules:
            if skip_scrape and mod["id"] == "02":
                results.append({"id": mod["id"], "status": "skipped", "output": str(mod["output"])})
                continue

            task = progress.add_task(f"Running module {mod['id']} ({mod['fn']})", total=None)
            try:
                fn = _load_module_function(mod["file"], mod["fn"])
                if mod["args"]:
                    fn(*mod["args"])
                else:
                    fn()
                results.append({"id": mod["id"], "status": "ok", "output": str(mod["output"])})
            except Exception as exc:
                output_path = Path(str(mod["output"]))
                cached = output_path.exists()
                console.print(f"[yellow]Module {mod['id']} failed:[/yellow] {exc}")
                console.print(traceback.format_exc())
                results.append(
                    {
                        "id": mod["id"],
                        "status": "failed_cached" if cached else "failed",
                        "output": str(mod["output"]),
                    }
                )
            finally:
                progress.remove_task(task)

    summary = Table(title="Turn.io GTM Agent Run Summary")
    summary.add_column("Module")
    summary.add_column("Status")
    summary.add_column("Output File")

    for row in results:
        summary.add_row(row["id"], row["status"], row["output"])

    console.print(summary)

    metrics_table = Table(title="Key Metrics Found")
    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")

    market_data = _safe_load_json(BRAZIL_MARKET_FILE) or {}
    derived = market_data.get("derived_metrics", {}) if isinstance(market_data, dict) else {}
    top_states = derived.get("top_10_states_private_market", [])

    comp_data = _safe_load_json(COMPETITIVE_FILE) or {}
    competitors = comp_data.get("competitors", []) if isinstance(comp_data, dict) else []

    partners_data = _safe_load_json(PARTNERS_FILE) or {}
    partner_categories = [k for k in partners_data.keys() if k != "notes"] if isinstance(partners_data, dict) else []

    metrics_table.add_row("Top states identified", str(len(top_states)))
    metrics_table.add_row("Competitors mapped", str(len(competitors)))
    metrics_table.add_row("Partner categories", str(len(partner_categories)))
    metrics_table.add_row("GTM markdown generated", "yes" if GTM_MARKDOWN_FILE.exists() else "no")
    metrics_table.add_row("GTM json generated", "yes" if GTM_JSON_FILE.exists() else "no")

    console.print(metrics_table)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn.io Brazil GTM planning agent")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip module 02 and use cached scrape data")
    parser.add_argument("--module", type=str, help="Run a single module by id (e.g., 02)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(skip_scrape=args.skip_scrape, single_module=args.module)
