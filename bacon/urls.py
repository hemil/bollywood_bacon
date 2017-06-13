from django.conf.urls import include, url
from django.contrib import admin
from .views import network_metrics, base_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', base_view.HomePageView.as_view(), name='home'),
    url(r'^about/?$', base_view.AboutPageView.as_view(), name='about'),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^v1/ping/?$', base_view.ping),
    url(r'^v1/shortest-path/?$', network_metrics.shortest_path, name='shortest-path'),
    url(r'^v1/degree-centrality/?$', network_metrics.degree_centrality, name='degree-centrality'),
    url(r'^v1/movie/actors/?$', network_metrics.actors_of_a_movie),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
