from django import forms
from django.forms import ModelForm
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'image', 'description', 'demo_link', 'source_link', 'tags']
        labels = {
            'title': 'Название проекта',
            'slug': 'Слаг',
            'image': 'Скриншот проекта',
            'tags': 'Теги',
            'description': 'Описание проекта',
            'demo_link': 'Демо-версия',
            'source_link': 'Исходный код на GitHub'
        }

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Оцените проект',
            'body': 'Добавьте комментарий'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
