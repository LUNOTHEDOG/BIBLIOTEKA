from django.contrib.auth.models import User

from .models import BookReview, Profilis, BookInstance
from django import forms

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Elektroninis paštas')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Vartotojo vardas'
        self.fields['username'].widget.attrs['placeholder'] = 'Vartotojo vardas'
        self.fields['username'].help_text = '150 ar mažiau simbolių. Tik raidės, skaitmenys ir @/./+/-/_.'
        self.fields['email'].widget.attrs['placeholder'] = 'Elektroninis paštas'





class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']



class DateInput(forms.DateInput):
    input_type = 'date'

class UserBookCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'reader', 'due_back', 'status']
        widgets = {'reader': forms.HiddenInput(), 'due_back': DateInput()}


class UserBookUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = [ 'reader', 'due_back']
        widgets = {'reader': forms.HiddenInput(), 'due_back': DateInput()}

