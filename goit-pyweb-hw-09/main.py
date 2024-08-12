import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def scrape_quotes():
    quotes = []
    authors = {}
    page = 1
    while True:
        soup = get_soup(f"{BASE_URL}/page/{page}/")
        page_quotes = soup.select(".quote")
        
        if not page_quotes:
            break

        for quote in page_quotes:
            text = quote.select_one(".text").get_text()
            author_name = quote.select_one(".author").get_text()
            tags = [tag.get_text() for tag in quote.select(".tag")]

            if author_name not in authors:
                author_url = quote.select_one(".author + a")["href"]
                author_soup = get_soup(f"{BASE_URL}{author_url}")
                born_date = author_soup.select_one(".author-born-date").get_text()
                born_location = author_soup.select_one(".author-born-location").get_text()
                description = author_soup.select_one(".author-description").get_text()

                authors[author_name] = {
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                }

            quotes.append({
                "quote": text,
                "author": author_name,
                "tags": tags
            })

        page += 1
    
    return quotes, list(authors.values())

def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

quotes, authors = scrape_quotes()

save_to_json("quotes.json", quotes)
save_to_json("authors.json", authors)
