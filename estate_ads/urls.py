from django.conf.urls import url
from django.http import HttpResponse

from estate_ads import views

urlpatterns = [
    url(r'', views.index_view),
]