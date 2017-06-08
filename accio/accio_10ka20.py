from neo4jrestclient.client import GraphDatabase
from string import ascii_uppercase
from bs4 import BeautifulSoup
import mechanize
import re
import requests
from common import create_movie_entities


def accio_10ka20_data():
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    actors_label = graph.labels.create("Actor")
    movies_label = graph.labels.create("Movie")
    source_url = "http://www.10ka20.com/"
    base_url = "http://www.10ka20.com/hindi-movies-by-name-{char}.html"
    urls = []
    for char in ascii_uppercase:
        urls.append(base_url.format(char=char))

    for url in urls:
        print "Search URL: {url}".format(url=url)
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")

        tables = soup.findAll("table")
        # All data of that url in wiki tables
        table = tables[-1]
        movies = table.findAll("a")
        for movie in movies:
            movie_url = source_url + movie["href"]
            print "Getting URL: {movie_url}".format(movie_url=movie_url)
            response = requests.get(movie_url)
            movie_soup = BeautifulSoup(response.text, "html.parser")
            try:
                tables = movie_soup.findAll("table")
                movie_info = tables[-1]
                rows = movie_info.findAll("tr")
                movie_cast = str(rows[2].findAll("td")[-1])[4:-5].strip()       # as per html structure
                actors = movie_cast.split(",")
                title = re.sub("[\(\[].*?[\)\]]", "", movie.contents[0])
                title = unicode(title).encode("utf-8").strip().capitalize()
                create_movie_entities(movies_label, actors_label, title, actors)
            except Exception:
                continue

accio_10ka20_data()
