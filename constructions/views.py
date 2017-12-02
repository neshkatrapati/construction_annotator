# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import JsonResponse
from django.core import serializers
import json
# Create your views here.
from .models import *
from .helpers import split_sentence, get_graph
from .forms import * 
from django.shortcuts import get_object_or_404

# Search Sentences, Constructions & Participants
# For C&P implements frequently occurs with. 
# Construction Influencers !

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



class ConstructionsView(ListView):
    model = ConstructionCategory
    template_name = 'constructions/cxnindex.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'constructions'  # Default: object_list
    paginate_by = 40
    queryset = ConstructionCategory.objects.all()  # D


class ConstructionParticipantsView(ListView):
    model = ConstructionParticipantType
    template_name = 'constructions/cxnpindex.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'participants'  # Default: object_list
    paginate_by = 40
    queryset = ConstructionParticipantType.objects.all()  # D



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




class CorpusFilesView(ListView):
    model = CorpusFile
    template_name = 'constructions/cfindex.html'
    context_object_name = 'corpus_files'
    paginate_by = 30
    queryset = CorpusFile.objects.all()

class CorpusFileView(ListView):
    model = Sentence
    template_name = 'constructions/index.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'sentences'  # Default: object_list
    paginate_by = 40
    

    def get_context_data(self, **kwargs):
        context = super(CorpusFileView, self).get_context_data(**kwargs)	
	corpus_file = get_object_or_404(CorpusFile, id=self.kwargs['id'])
	context['corpus_file'] = corpus_file
	return context
 
    def get_queryset(self):
    	self.corpus_file = get_object_or_404(CorpusFile, id=self.kwargs['id'])
        sentences = Sentence.objects.filter(corpus_file=self.corpus_file).order_by('treebank_id')
	sentences.corpus_file = self.corpus_file
	print sentences.corpus_file
	return sentences



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




def construction_participant_view(request, id):
	participant = ConstructionParticipantType.objects.get(pk = id)
	participants = ConstructionParticipantType.objects.all()
	allcs = ConstructionParticipant.objects.filter(type = participant)
	
	page = request.GET.get('page', 1)
	paginator = Paginator(allcs, 20)
	try:
            participant_instances = paginator.page(page)
	except PageNotAnInteger:
            participant_instances = paginator.page(1)
        except EmptyPage:
            participant_instances = paginator.page(paginator.num_pages)

        return render(request, 'constructions/cxnpviewer.html', {
        'participant' : participant,
	'participants' : participants,
	'cinstances' : participant_instances,
	'lead_color' : ''})


def construction_view(request, id):
	construction = ConstructionCategory.objects.get(pk = id)
	constructions = ConstructionCategory.objects.all()
	allcs = Construction.objects.filter(construction = construction)
	
	page = request.GET.get('page', 1)
	paginator = Paginator(allcs, 20)
	try:
            construction_instances = paginator.page(page)
	except PageNotAnInteger:
            construction_instances = paginator.page(1)
        except EmptyPage:
            construction_instances = paginator.page(paginator.num_pages)

        return render(request, 'constructions/cxnviewer.html', {
        'construction' : construction,
	'constructions' : constructions,
	'cinstances' : construction_instances,
	'lead_color' : ''})

def delete_others(let_stay, sentence, Model):
	d = Model.objects.filter(sentence = sentence).exclude(pk__in = let_stay)
	d.delete()

def add_construction(request):
	resp = {'status' : True}
	if request.POST:
		data = json.loads(request.POST['data'])
		sid = request.POST['sentence']
		sentence  = Sentence.objects.get(pk = sid)
		constructions = data['constructions']
		participants = data['participants']
		print participants
		new = False
		let_stay = []
		for ckey in constructions:
			construction = constructions[ckey]

			if 'model_id' in construction:
				# That means that this is not a new construction.
				conobj = Construction.objects.get(pk = construction['model_id'])
				
			else:
				conobj = Construction()
				#conobj.save()
				#conobj.participants.add(ConstructionParticipant())
				new	= True



			ctype = ConstructionCategory.objects.get(pk = int(ckey.split('_')[0]))			
			conobj.construction = ctype
			conobj.sentence = sentence
			conobj.span_start = construction['start']
			conobj.span_end = construction['stop']

			# conobj.participants = ''
			conobj.save()
			let_stay.append(conobj.id)

		delete_others(let_stay, sentence, Construction)
		let_stay = []
		for index, pkey in enumerate(participants):

			participant = participants[pkey]
			
			if 'model_id' in participant:
				# That means that this is not a new construction.
				partobj = ConstructionParticipant.objects.get(pk = participant['model_id'])
				#construction = ConstructionParticipant.constructions_set.get(pk = partobj.pk)
				#construction = Construction.objects.all().participants_set.get(pk = partobj.pk)				
				construction = partobj.construction_set.get()
			else:
				partobj = ConstructionParticipant()


				ckey = participant['construction']
				ctype = ConstructionCategory.objects.get(pk=int(ckey.split('_')[0]))
				cstart = ckey.split('_')[1]
				construction = Construction.objects.get(sentence = sentence, construction = ctype, 
					span_start = cstart)
			
			partobj.sentence = sentence
			partobj.span_start = participant['start']
			partobj.span_end = participant['stop']
			partobj.type = ConstructionParticipantType.objects.get(pk = int(participant['id']))
			partobj.save()
			let_stay.append(partobj.id)
			construction.participants.add(partobj)
		delete_others(let_stay, sentence,ConstructionParticipant)




	else:
		resp['status'] = False
	return JsonResponse(resp)
