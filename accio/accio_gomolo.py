from neo4jrestclient.client import GraphDatabase, Node
from neo4jrestclient.query import Q
from bs4 import BeautifulSoup
import re
import mechanize
import logging
import traceback


logger = logging.getLogger()
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(funcName)s(%(lineno)d) -- %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('logs/accio_data.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def accio_gomolo_data():
    graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="1123581321")
    actors_label = graph.labels.create("Actor")
    movies_label = graph.labels.create("Movie")
    # node_selector = NodeSelector(graph)

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
        replacements = (u'\t', ''), (u'\n', ''), (u'[u\'', ''), (u'\\xa0\\xa0\']', ''), (' and others', ''), (
            u'[u\"', ''), (u'\\xa0\\xa0\""]', '')

        for each_movie_html in rows[1:]:
            try:

                # import pdb
                # pdb.set_trace()
                soup = BeautifulSoup(str(each_movie_html), "html.parser")
                movie_html = list()
                for row in soup.findAll("td"):
                    movie_html.append(row)
                if len(movie_html) < 4:
                    continue

                movie_title = BeautifulSoup(str(movie_html[0]), "html.parser")
                title = movie_title.find('td').find('a')['title']
                title = unicode(title).encode("utf-8").strip().capitalize()
                movie_lookup = Q("name", iexact=title)
                movie_nodes = movies_label.filter(movie_lookup)
                if len(movie_nodes) > 0:
                    movie_node = movie_nodes[0]
                else:
                    movie_node = movies_label.create(name=unicode(title).encode("utf-8").strip().capitalize())

                # You have the Movie Node. Get or Create
                movie_cast = BeautifulSoup(str(movie_html[3]), "html.parser")
                actors_string = multiple_replace(str(movie_cast.findAll('td')[0].contents),
                                                 *replacements)  # Cleanup internet shit
                actors = actors_string.split(", ")
                for actor in actors:
                    actor = unicode(actor).encode("utf-8").strip().capitalize()
                    actor_lookup = Q("name", iexact=actor)
                    actor_nodes = actors_label.filter(actor_lookup)
                    if len(actor_nodes) > 0:
                        actor_node = actor_nodes[0]
                    else:
                        actor_node = actors_label.create(name=actor)

                    actor_node.Acted_In(movie_node)
                    print "Movie: {title} Actor: {actor}".format(title=title, actor=actor)

            except Exception as e:
                logger.error("ERROR!: {e}".format(e=e))
                print traceback.print_exc()
                exit()
accio_gomolo_data()
