from django.forms import ModelForm, ChoiceField, CharField, Form
from .models import * 
from django_select2.forms import Select2MultipleWidget, Select2Widget, ModelSelect2Widget

class ConstructionCategorySearchForm(Form):
	construction = ChoiceField(widget = ModelSelect2Widget(model = ConstructionCategory,search_fields = ['name__icontains'] ))