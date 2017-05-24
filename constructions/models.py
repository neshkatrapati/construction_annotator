# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from .helpers import *
# Create your models here.

class ConstructionParticipantType(models.Model):
	name = models.CharField(max_length=2000)
	description = models.TextField(null=True)
	color = ColorField(default = '#FF0000')
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return '/app/cxp/'+str(self.pk)


class ConstructionCategory(models.Model):
	name = models.CharField(max_length=2000)
	description = models.TextField(null=True)
	color = ColorField(default = '#FF0000')
	# Need to add Construction Form (Canonical Form) with Color Coding
	participants = models.ManyToManyField(ConstructionParticipantType)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return '/app/cx/'+str(self.pk)

class Sentence(models.Model):
	treebank_id = models.IntegerField()
	plain_form = models.TextField(null=True)
	treebank_form = models.TextField(null = True)

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return unicode(self.plain_form)

	def as_list(self):
		return split_sentence(self)

	def get_absolute_url(self):
		return '/app/s/' + str(self.id)

class ConstructionParticipant(models.Model):
	type = models.ForeignKey(ConstructionParticipantType)
	sentence = models.ForeignKey(Sentence)
	span_start = models.IntegerField()
	span_end = models.IntegerField()



	
	def __unicode__(self):
		return unicode(self.type.name)

class Construction(models.Model):
	sentence = models.ForeignKey(Sentence)
	construction = models.ForeignKey(ConstructionCategory)
	span_start = models.IntegerField()
	span_end = models.IntegerField()
	participants = models.ManyToManyField(ConstructionParticipant, null=True, blank=True)

	def __unicode__(self):
		if hasattr(self, 'construction'):
			return unicode(self.construction.name)
		else:
			return u'Dummy'
