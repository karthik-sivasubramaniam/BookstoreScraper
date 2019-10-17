from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd

tld = "http://books.toscrape.com"
next = ""

titles = []
prices = []
ratings = []
images = []

def extract_books(url):
    
    html = requests.get(url).text
    soup = bs4(html, "html.parser")
    listings = soup.find_all("article", "product_pod")

    for listing in listings:
        title = listing.find("h3").find("a")["title"]
        titles.append(title)
        rating = listing.find("p").attrs["class"][1]
        ratings.append(rating)
        price = listing.find("p","price_color").text.lstrip('Â')
        prices.append(price)
        image_path = listing.find("img", class_="thumbnail").attrs["src"]
        image = "/".join([tld, image_path])
        images.append(image)

    global next
    try:
        next = soup.find("li", class_="next").find("a").attrs["href"].lstrip("catalogue/")
    except AttributeError:
        next = None
        return next
    next = "catalogue/" + next

while next != None:
    url = "/".join([tld, next])
    extract_books(url)

data = {
    "titles": titles,
    "images": images,
    "prices": prices,
    "ratings": ratings
}

books = pd.DataFrame(data=data)
books.index += 1

print(books)
