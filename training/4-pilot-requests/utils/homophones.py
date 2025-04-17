import requests
from bs4 import BeautifulSoup
import re

def get_homophones(word):
    url_template = "https://www.homophone.com/search?page={}&type=&q={}"

    # Get the first page
    url = url_template.format(1, word)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find total pages
    try:
        pages_text = soup.find("div", attrs={"class": "col-sm-9"}).find("h5").text
        total_pages = int(pages_text.split("/")[-1].strip())
    except (AttributeError, ValueError):
        total_pages = 1  # Default to 1 if page info isn't found

    homophones = []

    # Iterate through all pages
    for page_no in range(1, total_pages + 1):
        url = url_template.format(page_no, word)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        raw_homophones = soup.find_all("div", attrs={"class": "well well-lg"})

        for elem in raw_homophones:
            word_buttons = elem.find_all("a", attrs={"class": "btn word-btn"})
            homophones.extend([btn.text for btn in word_buttons])

    homophones = list(set(homophones))
    # homophones = [h for h in homophones if not h.startswith(word)]
    return homophones


if __name__ == "__main__":
    word = "taxi"
    homophones = get_homophones(word)
    print(homophones)