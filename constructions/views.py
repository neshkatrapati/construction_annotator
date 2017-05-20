# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from .models import *
from .helpers import split_sentence




class SentenceView(ListView):
    model = Sentence
    template_name = 'constructions/index.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'sentences'  # Default: object_list
    paginate_by = 40
    queryset = Sentence.objects.all()  # D

def annotate(request, id):
	sentence = Sentence.objects.get(id = id)
	words = split_sentence(sentence)
	return render(request, 
		'constructions/annotate.html', 
		{'sentence': sentence,
		 'words':words})