from django.conf.urls import url
from django.contrib import admin

from .views import *


urlpatterns = [  
    url(r's/(?P<id>\d+)', annotate, name = "annotate"),
    url(r'cf/(?P<id>\d+)', CorpusFileView.as_view(), name = "corpus_file_index"),
    url(r'cx/$', ConstructionsView.as_view(), name = "construction_index"),
    url(r'cx/(?P<id>\d+)$', construction_view, name = "construction_view"),
    url(r'cxp/$', ConstructionParticipantsView.as_view(), name = "construction_participant_index"),
    url(r'cxp/(?P<id>\d+)$', construction_participant_view, name = "construction_participant_view"),
    url(r'^cc/$', ConstructionCategoryView.as_view(), name = "construction_categories"),
    url(r'^cp/(?P<id>\d+)$', ConstructionParticipantCategoryView.as_view(), name = "construction_participant_categories"),
    url(r'^ca/$', add_construction, name = "construction_add"),
    url(r'^$', CorpusFilesView.as_view(), name = "index"),

]
