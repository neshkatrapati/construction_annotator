# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from constructions.models import * 
# Register your models here.
#@admin.register(Sentence)
#class SentenceAdmin(admin.ModelAdmin):
	#fields = ('treebank_id',)
	#exclude = ('plain_form', 'treebank_form')
admin.site.register(Sentence)	
admin.site.register(ConstructionCategory)
admin.site.register(ConstructionParticipantType)