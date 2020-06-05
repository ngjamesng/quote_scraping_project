import requests
from bs4 import BeautifulSoup
from csv import writer

import random
from time import sleep

#
# section to scrape quotes
#
BASE_URL = "http://quotes.toscrape.com"
url = ""
quotes_list = []

while url or url is "":
    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.select(".quote")

    for quote in quotes:
        author = quote.find(class_="author").get_text()
        text = quote.find(class_="text").get_text()
        link = quote.find("a")["href"]

        quotes_list.append({
            "author": author,
            "text": text,
            "link": link
        })

    next_link = soup.find(class_="next")
    url = next_link.find("a")["href"] if next_link else None

    # seconds = round(random.uniform(1.0, 5.0), 2)
    # sleep(seconds)

print(len(quotes_list))


#
# Section to write to CSV file
#

# with open("quote_data.csv", "w") as csv_file:
#     csv_writer = writer(csv_file)
#     csv_writer.writerow(["author", "text", "link"])

#     for quote in quotes_list:
#         print(quote)
#         csv_writer.writerow([
#             quote["author"],
#             quote["text"],
#             quote["link"]
#         ])


