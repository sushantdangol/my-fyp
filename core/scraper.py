from bs4 import BeautifulSoup as bs
import requests

def scraper(url):
    response = requests.get(url, timeout=5)
    content = bs(response.content, "html.parser")
    story = ""

    for item in content.findAll('p'):
        story = story + " " + item.text


    return story
    print(story)

