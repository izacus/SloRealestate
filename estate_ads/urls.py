from django.conf.urls import patterns, url
from django.http import HttpResponse
import views

urlpatterns = patterns('',
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
    url(r'', views.index_view),
)