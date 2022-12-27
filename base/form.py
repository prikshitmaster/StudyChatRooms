from django.forms import ModelForm

from base.models import Room, Topic

from django import forms


class RoomModel(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host' , 'participants']


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
