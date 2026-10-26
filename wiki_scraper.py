
import os
import random
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

WIKI_SCRAPED_URLS = 0
WIKI_VISITED = set()

def get_links(bs):
    links = bs.find("div", {"id": "bodyContent"}).find_all(
        "a",
        href=re.compile(r"^(?:https://en\.wikipedia\.org)?/wiki/[^:#]+$"),
    )
    links = [link.get("href") for link in links]
    return [link for link in links if link not in WIKI_VISITED]

def scrape_article(path):
    """Recursively find links on Wikipedia page,
    then follow a random link, with artficial 3 sec delay.
    """
    global WIKI_SCRAPED_URLS
    global WIKI_VISITED

    WIKI_VISITED.add(path)
    # print(f"> Scraping {path!r} ...")
    # time.sleep(3)
    resp = requests.get(
        urljoin("https://en.wikipedia.org", path),
        headers={"User-Agent": "Mr.Robot-Linux_Machine"}
    )
    bs = BeautifulSoup(resp.text, "lxml")
    title = bs.find("h1").get_text(strip=True)
    print(f"Scraping {bs.find('h1').get_text(strip=True)} -> PID: {os.getpid()}")
    # links = bs.find("div", {"id": "bodyContent"}).find_all(
    #     "a",
    #     # href=re.compile("^(/wiki/)((?!:).)*$"),
    #     href = re.compile(r"^(?:https://en\.wikipedia\.org)?/wiki/[^:#]+$"),
    # )
    links = get_links(bs)

    if WIKI_SCRAPED_URLS >= 100:  # stop if the scraping limit hits
        return
    if len(links) > 0:
        new_article = links[random.randint(0, len(links) - 1)]
        WIKI_SCRAPED_URLS += 1
        scrape_article(new_article)
    else:
        print("No links found.")
