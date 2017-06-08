from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

from bacon.modules.utilities import get_shortest_path, get_degree_centrality, get_actors_of_a_movie


@csrf_exempt
@api_view(["GET"])
def shortest_path(request):
    name_one = request.GET.get("name_one")
    name_two = request.GET.get("name_two")
    if name_one is None and name_two is None:
        response_json = json.dumps({
            'status': 1,
            'data': "Invalid Data",
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
        return HttpResponse(response_json, content_type="application/json", status=400)

    result = get_shortest_path(name_one, name_two)

    response_json = json.dumps({
            'status': 1,
            'data': result.graph[0],
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def degree_centrality(request):
    name_one = request.GET.get("name_one")
    result = get_degree_centrality(name_one)
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
    result = get_actors_of_a_movie(name_one)
    response_json = json.dumps({
            'status': 1,
            'data': list(result),
            'instance_name': settings.INSTANCE_NAME,
            'count': 0
        })
    return HttpResponse(response_json, content_type="application/json")
