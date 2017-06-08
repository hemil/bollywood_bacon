from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from bs4 import BeautifulSoup
import mechanize
import re


def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

replacements = (u'\t', ''), (u'\n', ''), (u'[u\'', ''), (u'\\xa0\\xa0\']', ''), (' and others', ''), (
            u'[u\"', ''), (u'\\xa0\\xa0\""]', ''), (u'\r\n', ''), (u'<br>', ''), (u'Produced By:.*', ''), \
               (u'Directed By:.*', ''), (u'-', ''), (u'"', ''), (u'`', ''), (u'Music By:.*', ''), (u'<[^>]*>', ''), \
               (u'Lyrics:.*', ''),


def accio_wiki_data():
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    actors_label = graph.labels.create("Actor")
    movies_label = graph.labels.create("Movie")
    base_url = "https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_{year}"
    urls = []
    for year in xrange(1973, 2017):
        urls.append(base_url.format(year=year))
    for url in urls:
        print "Search URL: {url}".format(url=url)
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")

        tables = soup.findAll("table", {"class": "wikitable"})
        # All data of that url in wiki tables

        for table in tables:
            rows = table.findAll("tr")
            for row in rows:
                try:
                    # Each Movie is a Row
                    columns = row.findAll("td")
                    if len(columns) != 5:
                        # Remove the Header Row
                        continue
                    movie = columns[0].find("a")
                    if not movie:
                        continue
                    title = movie.contents[0]
                    title = multiple_replace(title, *replacements)
                    title = unicode(title).encode("utf-8").strip().title()

                    movie_lookup = Q("name", iexact=title)
                    movie_nodes = movies_label.filter(movie_lookup)
                    if len(movie_nodes) > 0:
                        movie_node = movie_nodes[0]
                    else:
                        movie_node = movies_label.create(name=title)

                    # You have the Movie Node. Get or Create
                    movie_cast = BeautifulSoup(str(columns[2]), "html.parser")
                    actors_links = movie_cast.find_all("a")

                    for actor_link in actors_links:
                        if "does not exist" not in unicode(actor_link["title"]).encode("utf-8"):
                            # if wiki page exists
                            actor = actor_link.contents[0]
                            actor = multiple_replace(actor, *replacements)
                            actor = unicode(actor).encode("utf-8").strip().title()
                            if actor:
                                actor_lookup = Q("name", iexact=actor)
                                actor_nodes = actors_label.filter(actor_lookup)
                                if len(actor_nodes) > 0:
                                    actor_node = actor_nodes[0]
                                else:
                                    actor_node = actors_label.create(name=actor)

                                actor_node.Acted_In(movie_node)
                                print "Movie: {title} Actor: {actor}".format(title=title, actor=actor)
                except UnicodeDecodeError:
                    continue


def accio_wiki_data_format_2():
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    actors_label = graph.labels.create("Actor")
    movies_label = graph.labels.create("Movie")
    base_url = "https://en.wikipedia.org/wiki/List_of_Bollywood_films_of_{year}"
    urls = []
    for year in xrange(2008, 2013):
        urls.append(base_url.format(year=year))
    for url in urls:
        print "Search URL: {url}".format(url=url)
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        soup = BeautifulSoup(browser.response().read(), "html.parser")

        tables = list(soup.findAll("table", {"class": "wikitable sortable jquery-tablesorter"}))
        tables.extend(list(soup.findAll("table", {"class": "wikitable"})))
        # All data of that url in wiki tables

        for table in tables:
            rows = table.findAll("tr")
            for row in rows:
                try:
                    # Each Movie is a Row
                    columns = row.findAll("td")
                    if not columns:
                        continue

                    if len(columns) < 3:
                        # Remove the Header Rows and side columns
                        continue
                    movie_column_index = 0
                    movie = columns[0].find("a")
                    if movie is None:
                        movie = columns[1].find("a")
                        movie_column_index = 1
                    if movie is None:
                        movie = columns[2].find("a")
                        movie_column_index = 2

                    if movie is None:
                        continue

                    try:
                        movie_cast = BeautifulSoup(str(columns[movie_column_index + 2]), "html.parser")
                    except IndexError:
                        continue

                    title = movie.contents[0]
                    title = multiple_replace(title, *replacements)
                    title = unicode(title).encode("utf-8").strip().title()

                    movie_lookup = Q("name", iexact=title)
                    movie_nodes = movies_label.filter(movie_lookup)
                    if len(movie_nodes) > 0:
                        movie_node = movie_nodes[0]
                    else:
                        movie_node = movies_label.create(name=title)

                    # You have the Movie Node. Get or Create
                    actors_links = movie_cast.find_all("a")

                    for actor_link in actors_links:
                        if "does not exist" not in unicode(actor_link.get("title", "does not exist")).encode("utf-8"):
                            # if wiki page exists
                            actor = actor_link.contents[0]
                            actor = multiple_replace(actor, *replacements)
                            actor = unicode(actor).encode("utf-8").strip().title()

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

accio_wiki_data()
accio_wiki_data_format_2()
