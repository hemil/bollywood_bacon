import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings


@api_view(['POST', 'GET', 'DELETE', 'PUT', 'HEAD'])
def ping(request):
    return HttpResponse(json.dumps({
        'status': 1,
        'data': [],
        'instance_name': settings.INSTANCE_NAME,
        'count': 0
    }), content_type="application/json")


from django.views.generic import TemplateView  # Import TemplateView


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"

