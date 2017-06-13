from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.shortcuts import render
from bacon.modules.utilities import get_shortest_path, get_degree_centrality, get_actors_of_a_movie

@csrf_exempt
@api_view(["GET"])
def shortest_path(request):
    showGraph=False;
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
    formattedResponse=json.dumps(formatNodesForShortestPath(response_json))
    # print(response_json)
    # print(render(request,'index.html', context))
    # return render(request,'index.html', context)

    return HttpResponse(formattedResponse, content_type="application/json")


def formatNodesForShortestPath(response_json):
    response=json.loads(response_json)
    nodes=[]
    links=[]
    code={
        'Movie':0,
        'Actor':1
    }
    if response['data']:
        if(response['data']['nodes']):
            for node in response['data']['nodes']:
                obj={
                    'id':node['id'],
                    'group':code[node['labels'][0]],
                    'text':node['properties']['name']
                }
                nodes.append(obj)
        if response['data']['relationships']:
            for rels in response['data']['relationships']:
                obj={
                    'source':rels['startNode'],
                    'target':rels['endNode'],
                    'value':3
                }
                links.append(obj)
    formattedResponse={
        'nodes':nodes,
        'links':links
    }
    return formattedResponse

   
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
