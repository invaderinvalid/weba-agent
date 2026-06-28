# weba-agent

An experimental autonomous web-scraping agent built with Python, OpenRouter, and Playwright. It runs a simple Observe → Reason → Act loop: the model decides when to navigate a page, the browser wrapper performs the action, and the result is fed back to the model until it produces a final answer.

## What it does

- Opens a visible Chromium browser with Playwright.
- Sends browser tool calls through an OpenRouter chat model.
- Navigates to a URL and extracts visible page text.
- Prints the final response in the terminal.

## Requirements

- Python 3.10+.
- An OpenRouter API key.
- Playwright with a Chromium browser installed.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the sample environment file and set your API key:

```bash
cp .example.env .env
```

4. Edit `.env` and set `OPENROUTER_API_KEY`.

5. Install the Playwright browser binaries if they are not already present:

```bash
playwright install
```

## Run

```bash
python main.py
```

The default entry point runs a demo task against `https://example.com` and reports the page heading.

## How it works

- `main.py` checks that `OPENROUTER_API_KEY` is set and starts the demo task.
- `agent.py` creates the OpenRouter client and runs the tool-calling loop.
- `browser_tools.py` launches Chromium, opens a page, and exposes navigation/content extraction helpers.
- `schemas.py` defines the tool schema passed to the model.

The agent currently exposes two tools:

- `navigate(url)` to open a page.
- `get_page_content()` to read visible text from the current page.

## Project structure

```text
agent.py          # Agent loop and OpenRouter client setup
browser_tools.py   # Playwright browser wrapper
main.py            # Script entry point and demo task
schemas.py         # Tool definitions for the model
requirements.txt   # Python dependencies
```

## Notes

- The browser is launched with `headless=False`, so a real window will open.
- The model is configured in `agent.py` through the `MODEL` constant.
- To change the behavior, edit the task string in `main.py` or call `run_agent()` from your own script.

## Troubleshooting

- If you see `OPENROUTER_API_KEY environment variable is not set`, add the key to `.env` or export it in your shell.
- If Playwright fails to launch Chromium, run `playwright install` again.
- If the model is unable to call tools, verify that the OpenRouter model you selected supports tool calling.
