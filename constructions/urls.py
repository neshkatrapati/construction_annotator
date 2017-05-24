from django.conf.urls import url
from django.contrib import admin

from .views import SentenceView, annotate, ConstructionCategoryView, ConstructionParticipantCategoryView


urlpatterns = [  
    url(r's/(?P<id>\d+)', annotate, name = "annotate"),
    url(r'^cc/$', ConstructionCategoryView.as_view(), name = "construction_categories"),
    url(r'^cp/(?P<id>\d+)$', ConstructionParticipantCategoryView.as_view(), name = "construction_participant_categories"),
    url(r'^$', SentenceView.as_view(), name = "index"),

]
