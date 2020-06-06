import requests
from bs4 import BeautifulSoup
from csv import writer

import random
from time import sleep

'''
section to scrape quotes
'''
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

quote = random.choice(quotes_list)
print(quote["text"])
print(quote["author"])

guesses_remaining = 5
guess = ""
while guess.lower() != quote["author"].lower() and guesses_remaining > 0:

    guess = input(
        f"Who's quote is this? Guesses remaining: {guesses_remaining} ")

    guesses_remaining -= 1

    if guesses_remaining == 3:
        response = requests.get(f"{BASE_URL}{quote['link']}")
        soup = BeautifulSoup(response.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"hint: the author was born on {birth_date} {birth_place}")
    elif guesses_remaining == 2:
        first_initial = quote['author'][0]
        print(
            f"hint: the author's first name starts with: {first_initial}")
    elif guesses_remaining == 1:
        last_initial = quote['author'].split(' ')[1][0]
        print(f"hint: the author's last name starts with: {last_initial}")
    else:
        print(f"sorry, no more guesses. the answer is {quote['author']}")


'''
Section to write to CSV file
'''

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
