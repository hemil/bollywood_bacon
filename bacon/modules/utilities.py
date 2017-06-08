from neo4jrestclient.client import GraphDatabase
from django.conf import settings


def run_query(query):
    graph = GraphDatabase(settings.NEO4J_URL, username=settings.NEO4J_USER_NAME, password=settings.NEO4J_PASSWORD)
    result = graph.query(q=query, data_contents=True)
    return result


def get_shortest_path(name_one, name_two):
    q = """
        MATCH p=shortestPath((bacon:Actor {{name:"{name_one}"}})-[*]-(meg:Actor {{name:"{name_two}"}}))
        RETURN p
        """.format(name_one=name_one, name_two=name_two)
    result = run_query(q)
    return result


def get_degree_centrality(name_one):
    q = """
        MATCH (ab:Actor {{name:"{name_one}"}})-[:Acted_In]->(m)<-[:Acted_In]-(coActors)
        RETURN Distinct(coActors.name), m.name
        """.format(name_one=name_one)
    result = run_query(q)
    return result


def get_actors_of_a_movie(name_one):
    q = """
        MATCH (p:Actor)-[:Acted_In]->(m:Movie)
        WHERE m.name=~"(?i){name_one}"
        RETURN Distinct(p.name)
        """.format(name_one=name_one)
    result = run_query(q)
    return result
