import requests
from bs4 import BeautifulSoup
from csv import DictWriter, DictReader

import random
from time import sleep

'''
section to scrape quotes
'''
BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    '''
     scrapes for results, and then returns the list of results. 
    '''
    quotes_list = []
    url = ""
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

        seconds = round(random.uniform(1.0, 5.0), 2)
        sleep(seconds)
    return quotes_list


def write_quotes(quotes_list):
    ''' 
    takes in a list and writes the results into a csv file.
    '''
    with open("quote_data.csv", "w") as csv_file:
        headers = ["author", "text", "link"]
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()

        for quote in quotes_list:
            print(quote)
            csv_writer.writerow(quote)


def read_quotes(filename):
    ''' takes in a string and reads the file name, and returns the results in a list format. 
    '''
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    ''' takes in the list of quotes, and starts the game. 
    '''
    quote = random.choice(quotes)
    print(quote["text"])
    print(quote["author"])

    guesses_remaining = 5
    guess = ""
    while guess.lower() != quote["author"].lower() and guesses_remaining > 0:

        guess = input(
            f"Who's quote is this? Guesses remaining: {guesses_remaining} \n")

        guesses_remaining -= 1

        if (guess.lower() == quote["author"].lower()):
            print("YOU GUESSED RIGHT!")
            break

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
        elif guesses_remaining == 0:
            print(f"sorry, no more guesses. the answer is {quote['author']}")

    play_again = ""
    while play_again.lower() not in ("y", "yes", "no", "n"):
        play_again = input("would you like to play again? (y/n)")

        if play_again.lower() in ("yes", "y"):
            return start_game(quotes)
        elif play_again.lower() in ("no", "n"):
            print("okay goodbye.")


# quotes = scrape_quotes()
# write_quotes(quotes)

def get_quotes(read, write, scrape):
    ''' tries to read from "quote_data.csv. 
    If the file cannot be found, 
    it will then scrape for results, save the results, and return the results.
    '''
    try:
        # see if there is already data in the csv file
        return read("quote_data.csv")
    except FileNotFoundError:
        #  if not, scrape, save, and return the results
        quotes = scrape()
        write(quotes)
        return quotes


quotes = get_quotes(read_quotes, write_quotes, scrape_quotes)
start_game(quotes)

'''
Section to write to CSV file
'''
