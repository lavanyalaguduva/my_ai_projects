**Day 1:** Scripts under `day1/` fetch HTML with `requests` and Beautiful Soup (`utils.scraper.fetch_website_contents`), then call OpenAI chat completions for website summaries, test-case ideas, and property-style extraction from the scraped text.

**Day 2:** 
 - `day2/chat_completion_api.py` exercises chat completions with a raw OpenAI HTTP `POST`, the official `OpenAI` Python client, and Gemini via Google’s OpenAI-compatible base URL. 
 - `day2/summarize_website_ollama.py` summarizes a URL using a local model through [Ollama](https://ollama.com)’s OpenAI-compatible API (`OpenAI` client + `base_url=http://localhost:11434/v1`); that script loads pages with **Playwright** (`utils.scraper.fetch_website_contents_playwright`) so JavaScript-rendered content is included.

**Setup:** From the repo root, use `uv sync` so the `utils` package is installed in editable mode. For Playwright, run `uv run playwright install chromium` once (or `.venv/bin/playwright install chromium` if the venv is active). Ollama must be running locally with a pulled model (e.g. `llama3.2`) matching the script.
