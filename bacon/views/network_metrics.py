from django.http import HttpResponse
from rest_framework.decorators import api_view
from neo4jrestclient.client import GraphDatabase, Node, Relationship
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from bacon.modules.error_response import get_http_response


@csrf_exempt
@api_view(["GET"])
def shortest_path(request):
    name_one = request.GET.get("name_one").title()
    name_two = request.GET.get("name_two").title()
    if name_one is None and name_two is None:
        return get_http_response(status_code=400, message="Invalid Data")

    graph = GraphDatabase("http://localhost:7474/db/data/", username=settings.NEO_USER,
                          password=settings.NEO_PASSWORD)
    q = """
        MATCH p=shortestPath((bacon:Actor {{name:"{name_one}"}})-[*]-(meg:Actor {{name:"{name_two}"}}))
        RETURN p
        """.format(name_one=name_one, name_two=name_two)

    result = graph.query(q=q, data_contents=True)
    try:
        response_json = json.dumps({
                'status': 1,
                'data': result.graph[0],
                'instance_name': settings.INSTANCE_NAME,
                'count': 0
            })
    except TypeError:
        return get_http_response(status_code=404, message="No info found about {name_one} and {name_two}".format(
            name_one=name_one, name_two=name_two))

    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def degree_centrality(request):
    name_one = request.GET.get("name_one").title()
    graph = GraphDatabase("http://localhost:7474/db/data/", username=settings.neo4j_username,
                          password=settings.neo4j_password)
    q = """
        MATCH (ab:Actor {{name:"{name_one}"}})-[:Acted_In]->(m)<-[:Acted_In]-(coActors)
        RETURN Distinct(coActors.name), m.name
        """
    result = graph.query(q=q.format(name_one=name_one), data_contents=True)
    response_json = json.dumps({
            'status': 1,
            'data': list(result),
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def actors_of_a_movie(request):
    name_one = request.GET.get("name_one")
    graph = GraphDatabase("http://localhost:7474/db/data/", username=settings.neo4j_username,
                          password=settings.neo4j_password)
    q = """
        MATCH (p:Actor)-[:Acted_In]->(m:Movie)
        WHERE m.name=~"(?i){name_one}"
        RETURN Distinct(p.name)
        """
    result = graph.query(q=q.format(name_one=name_one), data_contents=True)
    response_json = json.dumps({
            'status': 1,
            'data': list(result),
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    return HttpResponse(response_json, content_type="application/json")
