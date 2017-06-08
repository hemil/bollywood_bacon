from neo4jrestclient.client import GraphDatabase
from bs4 import BeautifulSoup
import mechanize
from common import create_movie_entities


def accio_gomolo_data():
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    actors_label = graph.labels.create("Actor")
    movies_label = graph.labels.create("Movie")

    char_list = ['$']
    for i in xrange(65, 91):
        # Searching for Movies containing these characters. Forming search URLs
        char_list.append(str(unichr(i)))

    for char in char_list:
        url = 'http://www.gomolo.com/indian-movies-list-films-database?SearchChar={char}'.format(char=char)
        print "Search URL: {url}".format(url=url)
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")

        tables = soup.findAll('table')
        table = tables[1]
        rows = list()
        for row in table.findAll("tr"):
            rows.append(row)

        for each_movie_html in rows[1:]:
            try:
                soup = BeautifulSoup(str(each_movie_html), "html.parser")
                movie_html = list()
                for row in soup.findAll("td"):
                    movie_html.append(row)
                if len(movie_html) < 4:
                    continue

                movie_title = BeautifulSoup(str(movie_html[0]), "html.parser")
                title = movie_title.find('td').find('a')['title']
                title = unicode(title).encode("utf-8").strip().capitalize()

                movie_cast = BeautifulSoup(str(movie_html[3]), "html.parser")
                actors_string = str(movie_cast.findAll('td')[0].contents)
                actors = actors_string.split(", ")

                create_movie_entities(movies_label, actors_label, title, actors)
            except Exception:
                continue
accio_gomolo_data()
