import requests
from bs4 import BeautifulSoup
from random import choice


response = requests.get("http://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, "html.parser")

