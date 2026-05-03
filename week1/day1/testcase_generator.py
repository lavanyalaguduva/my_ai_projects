import os
from dotenv import load_dotenv
import openai
from IPython.display import Markdown, display
from openai import OpenAI

from utils.scraper import fetch_website_contents

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

system_prompt = """
You are a test case generator for a website.
You will be given the contents of a website, and you will need to generate a list of test cases for the website.
The test cases should be in the format of a list of dictionaries, with the following keys:
- name: the name of the test case
- description: a description of the test case
- expected_result: the expected result of the test case
- actual_result: the actual result of the test case
- status: the status of the test case (passed, failed, or skipped)
- error_message: the error message of the test case if it failed
"""

user_prompt_prefix = """
Here are the contents of a website.
Generate a list of test cases for this website.
The test cases should be in the format of a list of dictionaries, with the following keys:
- name: the name of the test case
- description: a description of the test case
- expected_result: the expected result of the test case
- actual_result: the actual result of the test case
- status: the status of the test case (passed, failed, or skipped)
- error_message: the error message of the test case if it failed

"""
def testcase_generator(url):
    website_contents = fetch_website_contents(url)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website_contents},
    ]
    response =openai.chat.completions.create(model="gpt-5-nano", messages=messages)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def display_testcases(url):
    summary = testcase_generator(url)
    display(Markdown(summary))

display_testcases("https://www.cnn.com")