from django import forms
from django.contrib.auth.models import User
from .models import Comments, VoxPopuli


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class CommentForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Comments
        fields = ('name', 'text')

###################################################################################################
#                                   НАРОДНОЕ ГОЛОСОВАНИЕ
###################################################################################################


# class VoxPopuliForm(forms.ModelForm):
#     """Форма голосования"""
#     CHOICES = [('За', 'За'),
#                ('Против', 'Против'),
#                ('Воздержался', 'Воздержался')]
#     result = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), label='Проголосуйте по этому закону')
#
#     class Meta:
#         model = VoxPopuli
#         fields = ['result']

