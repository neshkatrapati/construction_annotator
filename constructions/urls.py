from django.conf.urls import url
from django.contrib import admin

from .views import SentenceView, annotate

urlpatterns = [  
    url(r's/(?P<id>\d+)', annotate, name = "annotate"),
    url(r'', SentenceView.as_view(), name = "index"),

]
