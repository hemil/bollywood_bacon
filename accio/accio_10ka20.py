from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from string import ascii_uppercase
from bs4 import BeautifulSoup
import mechanize
import re
import requests


def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

replacements = (u'\t', ''), (u'\n', ''), (u'[u\'', ''), (u'\\xa0\\xa0\']', ''), (' and others', ''), (
            u'[u\"', ''), (u'\\xa0\\xa0\""]', ''), (u'\r\n', ''), (u'<br>', ''), (u'Produced By:*', ''), \
               (u'Directed By:*', ''), (u'-', ''), (u'"', ''), (u'`', '')


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
                # movie_cast = movie_cast.replace(".", ",")
                title = re.sub("[\(\[].*?[\)\]]", "", movie.contents[0])
                title = unicode(title).encode("utf-8").strip().capitalize()
                movie_lookup = Q("name", iexact=title)
                movie_nodes = movies_label.filter(movie_lookup)
                if len(movie_nodes) > 0:
                    movie_node = movie_nodes[0]
                else:
                    movie_node = movies_label.create(name=title)

                # You have the Movie Node. Get or Create
                actors = movie_cast.split(",")
                for actor in actors:
                    actor = actor.strip()
                    actor = multiple_replace(actor, *replacements)
                    if actor:
                        actor = unicode(actor).encode("utf-8").strip().capitalize()
                        actor_lookup = Q("name", iexact=actor)
                        actor_nodes = actors_label.filter(actor_lookup)
                        if len(actor_nodes) > 0:
                            actor_node = actor_nodes[0]
                        else:
                            actor_node = actors_label.create(name=actor)

                        actor_node.Acted_In(movie_node)
                        print "Movie: {title} Actor: {actor}".format(title=title, actor=actor)
            except Exception:
                continue

accio_10ka20_data()
