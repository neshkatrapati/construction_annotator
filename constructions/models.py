# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
# Create your models here.

class ConstructionParticipantType(models.Model):
	name = models.CharField(max_length=2000)
	description = models.TextField(null=True)
	color = ColorField(default = '#FF0000')
	def __str__(self):
		return self.name

class ConstructionCategory(models.Model):
	name = models.CharField(max_length=2000)
	description = models.TextField(null=True)
	color = ColorField(default = '#FF0000')
	# Need to add Construction Form (Canonical Form) with Color Coding
	participants = models.ManyToManyField(ConstructionParticipantType)

	def __str__(self):
		return self.name

class Sentence(models.Model):
	treebank_id = models.IntegerField()
	plain_form = models.TextField(null=True)
	treebank_form = models.TextField(null = True)

	def __str__(self):
		return self.plain_form

	def __unicode__(self):
		return self.plain_form.encode('utf-8')


	def get_absolute_url(self):
		return '/app/s/' + str(self.id)

class ConstructionParticipant(models.Model):
	type = models.ForeignKey(ConstructionParticipantType)
	sentence = models.ForeignKey(Sentence)
	span_start = models.IntegerField()
	span_end = models.IntegerField()

class Construction(models.Model):
	sentence = models.ForeignKey(Sentence)
	construction = models.ForeignKey(ConstructionCategory)
	span_start = models.IntegerField()
	span_end = models.IntegerField()
	participants = models.ManyToManyField(ConstructionParticipant)
