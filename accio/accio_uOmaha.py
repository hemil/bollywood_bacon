'''
from a guy. 1931 to 1999 movies
'''
from bs4 import BeautifulSoup, SoupStrainer
import mechanize
from neo4jrestclient.client import GraphDatabase
from common import create_movie_entities

graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
actors_label = graph.labels.create("Actor")
movies_label = graph.labels.create("Movie")

root = 'http://faculty.ist.unomaha.edu/pdasgupta/allmovies/'
browser = mechanize.Browser()
browser.open(root)
collection_links = []
movies = []
soup = BeautifulSoup(browser.response(), "html.parser", parse_only=SoupStrainer('a'))

for link in soup:
    if link.has_attr('href'):
        collection_links.append(root + link['href'])
del collection_links[-1]
del collection_links[-1]
'''
links list has all the links which contains the movies.
'''

for collection_link in collection_links[20:]:
    print "Search URL: {url}".format(url=collection_link)
    browser.open(collection_link)
    soup = BeautifulSoup(browser.response(), "html.parser")
    for movie_html in soup.findAll('a', href=True):
        movie_link = movie_html["href"]
        try:
            browser.open(movie_link)

            movie_info_soup = BeautifulSoup(browser.response(), "html.parser")
            movie_info = movie_info_soup.find_all('p')[0].contents
        except Exception as e:
            print type(e)
            continue

        title = movie_html.get_text()[:-6]
        title = unicode(title).encode("utf-8").strip().capitalize()

        try:
            actors_one = unicode(movie_info[1]).encode("utf-8")
            actors_two = unicode(movie_info[2]).encode("utf-8").split("<br>")[1].strip()
            actors = actors_one.split(",")
            actors.extend(actors_two.split(","))
        except Exception:
            pass
        if not actors:
            continue

        create_movie_entities(movies_label, actors_label, title, actors)
