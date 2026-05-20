# turn_gtm_agent

Modular research and GTM planning agent for Turn.io's Brazil market entry.

## Project Goal

This project scrapes public data, analyzes the Brazilian healthcare market, maps competitors and potential partners, and generates an executive GTM briefing.

## Setup

1. Clone the repository.
2. Move into the project directory:
   ```bash
   cd turn_gtm_agent
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Playwright browsers:
   ```bash
   playwright install
   ```
5. Set your OpenAI API key in a `.env` file:
   ```env
   OPENAI_API_KEY=your_key_here
   ```

## Usage

Run full pipeline:

```bash
python main.py
```

Run a single module:

```bash
python main.py --module 02
```

Skip scraping and use cached data:

```bash
python main.py --skip-scrape
```

## Outputs

- Intermediate JSON files: `data/`
- Executive GTM briefing:
  - `outputs/turn_io_brazil_gtm.md`
  - `outputs/turn_io_brazil_gtm.json`
