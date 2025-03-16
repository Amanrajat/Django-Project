from django import forms 
from .models import Tweet
from .models import comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class TweetForm(forms.ModelForm):
    class Meta:
      model =Tweet
      fields=['text','photo']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class meta:
       model = User
       fields = ('username' , 'email' , 'passwor1' , 'password2' )

class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['text', 'photo']       
        