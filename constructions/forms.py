from django.forms import ModelForm, ChoiceField, CharField, Form, FileField, BooleanField
from django.contrib.admin.widgets import AdminFileWidget
from .models import * 
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget
from insert_sentences import *


class ConstructionCategorySearchForm(Form):
	construction = ChoiceField(widget = ModelSelect2Widget(model = ConstructionCategory,search_fields = ['name__icontains'] ))


class CorpusFileForm(ModelForm):
	corpus_file_field = FileField()	
	is_ssf = BooleanField(required=False)
	
	def save(self, commit=True):
		corpus_file_f = self.cleaned_data.get('corpus_file_field', None)
		is_ssf = self.cleaned_data.get('is_ssf', None)
		corpus_file = self.instance
		corpus_file.save()
		if not is_ssf:
			insert_plain(corpus_file_f.file, corpus_file)
		else:
			insert_from_fobj(corpus_file_f.file, corpus_file)	
		print corpus_file_f.file, is_ssf
		return super(CorpusFileForm, self).save(commit=commit)

	class Meta:
		model = CorpusFile
		fields = '__all__'
