import requests
from bs4 import BeautifulSoup
from random import choice


response = requests.get("http://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.select(".quote")

quotes_list = []
for quote in quotes:
    author = quote.find(class_="author").text
    text = quote.find(class_="text").text
    href = quote.find("a")["href"]
    quotes_list.append({"author": author, "text": text, "href": href})

random_quote = choice(quotes_list)
print(random_quote)