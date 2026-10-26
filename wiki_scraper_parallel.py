
import os
import random
import re
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

def task_delegator(task_queue, urls_queue):
    # Initialize with a task for each process
    visited = ["/wiki/Kevin_Bacon", "/wiki/"]
    task_queue.put("/wiki/Kevin_Bacon")
    task_queue.put("/wiki/Monty_Python")

    while True:
        # Check to see if there are new links in the
        #  urls_queue for processing
        if not urls_queue.empty():
            links = [link for link in urls_queue.get() if link not in visited]
            for link in links:
                # Add new link to the task_queue
                task_queue.put(link)


def get_links(bs):
    links = bs.find("div", {"id": "bodyContent"}).find_all(
        "a",
        href=re.compile(r"^(?:https://en\.wikipedia\.org)?/wiki/[^:#]+$"),
    )
    return [link.get("href") for link in links]


def scrape_article(task_queue, urls_queue):
    while True:
        while task_queue.empty():
            time.sleep(0.1)
        path = task_queue.get()
        resp = requests.get(
            urljoin("https://en.wikipedia.org", path),
            headers={"User-Agent": "Mr.Robot-Linux_Machine"}
        )
        bs = BeautifulSoup(resp.text, "lxml")
        print(f"Scraping {bs.find('h1').get_text(strip=True)} -> PID: {os.getpid()}")
        links = get_links(bs)
        # Send these to the delegator for processing
        urls_queue.put(links)
