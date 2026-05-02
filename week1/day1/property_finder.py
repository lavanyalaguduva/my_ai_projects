import os
from dotenv import load_dotenv
import openai
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

# TODO: revisit when I learn MCP as it needs a search tool
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

system_prompt = """
You are a property finder for a website.
You will be given the contents of a website, and you will need to find properties for the website.
The properties should be in the format of a list of dictionaries, with the following keys:
- name: the name of the property
- description: a description of the property
- price: the price of the property
- beds: the number of beds of the property
- bathrooms: the number of bathrooms of the property
- type: the type of the property
- url: the url of the property
"""

user_prompt_prefix = """
Here are the contents of a website.
Find properties for this website.
The properties should be in the format of a list of dictionaries, with the following keys:
- name: the name of the property
- description: a description of the property
- beds: the number of beds of the property
- bathrooms: the number of bathrooms of the property
- type: the type of the property
- url: the url of the property
- rental_price: the rental price of the property
- purchase_price: the purchase price of the property
"""
def property_finder(
    url,
    type: str = "",
    min_beds: int = 0,
    rental_min_price: int | str = 0,
    purchase_min_price: int | str = 0,
):
    website_contents = fetch_website_contents(url)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",  "content": user_prompt_prefix + website_contents + f"The type of the property is {type}, the minimum number of beds is {min_beds}, the minimum rental price is {rental_min_price}, the minimum purchase price is {purchase_min_price}"},
    ]
    response =openai.chat.completions.create(model="gpt-5-nano", messages=messages)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def display_properties(
    url,
    type: str = "",
    min_beds: int = 0,
    rental_min_price: int | str = 0,
    purchase_min_price: int | str = 0,
):
    summary = property_finder(url, type, min_beds, rental_min_price, purchase_min_price)
    display(Markdown(summary))

display_properties("https://www.rightmove.co.uk", type="house",min_beds=2,rental_min_price="2000")