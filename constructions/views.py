# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
from .models import *
from .helpers import split_sentence, get_graph
from .forms import * 


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        

        return JsonResponse(
            self.get_data(context),
            safe = False,
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """

        pass


class ConstructionCategoryView(JSONResponseMixin, ListView):
	model = ConstructionCategory
	queryset = ConstructionCategory.objects.all()
	context_object_name = 'construction_categories'

	def get_data(self, context):
		serialized = serializers.serialize('json', context['construction_categories'])
		return serialized

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)

class ConstructionParticipantCategoryView(JSONResponseMixin, ListView):
	model = ConstructionParticipantType
	
	context_object_name = 'construction_participant_categories'

	def get_queryset(self, **kwargs):
		parts = ConstructionCategory.objects.filter(id = self.kwargs['id']).values_list('participants', flat=True)
		cps = ConstructionParticipantType.objects.filter(pk__in = parts)
		
		return cps

	def get_data(self, context):
		serialized = serializers.serialize('json', context['construction_participant_categories'])
		return serialized

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)

class SentenceView(ListView):
    model = Sentence
    template_name = 'constructions/index.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'sentences'  # Default: object_list
    paginate_by = 40
    queryset = Sentence.objects.all()  # D

def annotate(request, id):
	sentence = Sentence.objects.get(id = id)
	words = split_sentence(sentence)
	concats = ConstructionCategory.objects.all()
	conform = ConstructionCategorySearchForm()
	png_path = get_graph(sentence.treebank_form)
	constructions = Construction.objects.filter(sentence = id)
	participants = ConstructionParticipant.objects.filter(pk__in = constructions.values('participants'))
	return render(request, 
		'constructions/annotate.html', 
		{'sentence': sentence,
		 'words':words,
		 'constructions' : constructions,
		 'participants' : participants,
		 'concats' : concats,
		 'conform' : conform,
		 'image':png_path})