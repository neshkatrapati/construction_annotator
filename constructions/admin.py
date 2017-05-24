# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from constructions.models import * 
#from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

# Register your models here.


class ConstructionParticipantInline(admin.StackedInline):
	model = ConstructionParticipant


class ConstructionInline(admin.StackedInline):
	model = Construction
	filter_horizontal = ('participants',)
	inlines = [ ConstructionParticipantInline ]


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):

	list_filter = ('treebank_id',)

	inlines = [ ConstructionParticipantInline, ConstructionInline]
	#fields = ('treebank_id',)
	#exclude = ('plain_form', 'treebank_form')

#admin.site.register(Sentence)	
admin.site.register(ConstructionCategory)

# @admin.register(Construction)
# class ConstructionAdmin(admin.ModelAdmin):
# 	 filter_horizontal = ('sentence',)
#	#fields = ('construction', 'span_start', 'span_end')
#	exclude = ('sentence',)

#admin.site.register(Construction)
admin.site.register(ConstructionParticipantType)
#admin.site.register(ConstructionParticipant)