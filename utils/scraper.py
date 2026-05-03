import re

import requests
from bs4 import BeautifulSoup

# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def _document_text_from_html(html: str) -> str:
    parser = BeautifulSoup(html, "html.parser")
    title = parser.title.string if parser.title else "Untitled"
    if parser.body:
        for irrelevant in parser.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = parser.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title + "\n\n" + text


def fetch_website_contents(url: str) -> str:
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    return _document_text_from_html(response.text)


def fetch_website_contents_playwright(url: str, *, timeout_ms: int = 60_000) -> str:
    """Load the page in a real browser so JS-rendered content is included."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="load", timeout=timeout_ms)
            html = page.content()
        finally:
            browser.close()
    return _document_text_from_html(html)
