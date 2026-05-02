import requests
from bs4 import BeautifulSoup

# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents(url):
    response = requests.get(url, headers=headers)
    parser = BeautifulSoup(response.text, 'html.parser')
    title = parser.title.string if parser.title else "Untitled"
    if parser.body:
        for irrelevant in parser.body(['script','style','img','input']):
            irrelevant.decompose()
        text = parser.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title +"\n\n" + text)