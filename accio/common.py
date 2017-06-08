from neo4jrestclient.query import Q
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
               (u'Lyrics:.*', ''), (u'Producer.*', ''), (u'(', ''), (u')', '')


def create_movie_entities(movies_label, actors_label, title, actors):
    title = title.title()
    title = multiple_replace(title, *replacements)
    title = re.sub(r'[0-9]*', '', title)
    movie_lookup = Q("name", iexact=title)
    movie_nodes = movies_label.filter(movie_lookup)
    if len(movie_nodes) > 0:
        movie_node = movie_nodes[0]
    else:
        movie_node = movies_label.create(name=title)

    # You have the Movie Node. Get or Create
    for actor in actors:
        try:
            actor = actor.strip()
            actor = multiple_replace(actor, *replacements)
            actor = re.sub(r'[0-9]*', '', actor)
            if actor:
                actor = unicode(actor).encode("utf-8").strip().title()
                actor_lookup = Q("name", iexact=actor)
                actor_nodes = actors_label.filter(actor_lookup)
                if len(actor_nodes) > 0:
                    actor_node = actor_nodes[0]
                else:
                    actor_node = actors_label.create(name=actor)

                actor_node.Acted_In(movie_node)
                print "Movie: {title} Actor: {actor}".format(title=title, actor=actor)
        except (UnicodeDecodeError):
            continue
        except Exception as e:
            print "Movie: {title} Actor: {actor}".format(title=title, actor=actor)
            print e
            continue
