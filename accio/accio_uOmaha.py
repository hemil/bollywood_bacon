'''
from a guy. 1931 to 1999 movies
'''
import re

from bs4 import BeautifulSoup, SoupStrainer
import mechanize
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q


def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

replacements = (u'\t', ''), (u'\n', ''), (u'[u\'', ''), (u'\\xa0\\xa0\']', ''), (' and others', ''), (
            u'[u\"', ''), (u'\\xa0\\xa0\""]', ''), (u'\r\n', ''), (u'<br>', ''), (u'Produced By:*', ''), \
               (u'Directed By:*', ''), ('.', ',')

graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="root")
actors_label = graph.labels.create("Actor")
movies_label = graph.labels.create("Movie")

root = 'http://faculty.ist.unomaha.edu/pdasgupta/allmovies/'
browser = mechanize.Browser()
browser.open(root)
collection_links = []
movies = []
soup = BeautifulSoup(browser.response(), "html.parser", parse_only=SoupStrainer('a'))
# x = PrettyTable(['link'])

for link in soup:
    if link.has_attr('href'):
        collection_links.append(root + link['href'])
del collection_links[-1]
del collection_links[-1]
'''
links list has all the links which contains the movies.
'''

for collection_link in collection_links[2:]:
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
            pass

        title = movie_html.get_text()[:-6]
        title = unicode(title).encode("utf-8").strip().title()
        if not re.match("^[a-zA-Z0-9 ]*$", title):
            print "Missing movie: {title}".format(title=title)
            continue
        movie_lookup = Q("name", iexact=title)
        movie_nodes = movies_label.filter(movie_lookup)
        try:
            if len(movie_nodes) > 0:
                movie_node = movie_nodes[0]
            else:
                movie_node = movies_label.create(name=title)

            actors_one = unicode(movie_info[1]).encode("utf-8")
            actors = actors_one.split(",")
        except Exception:
            continue

        try:
            actors_two = unicode(movie_info[2]).encode("utf-8").split("<br>")[1].strip()
            actors.extend(actors_two.split(","))
        except IndexError:
            "Only one line of actors"
            pass
        for actor_source in actors:
            try:
                actor = multiple_replace(actor_source, *replacements)
                actor = unicode(actor).encode("utf-8").strip().title()
                if not re.match("^[a-zA-Z0-9 ]*$", actor):
                    print "Missing movie: {title} and actor: {actor}".format(title=title, actor=actor)
                    continue
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
