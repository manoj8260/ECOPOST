from django import forms
from .models import * 
class UserModel(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name','last_name','email','username','password']
        help_texts={'username':' '}

        def clean_username(self):
            username=self.cleaned_data.get('username')
            if len(username)>6:
                return username
            return None

 
class ProfileModel(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['username','bio','website']
        gender = [('Male', 'Male'),
                ('Female', 'Female'),
        ]
        widgets = {'gender': forms.RadioSelect(choices=gender)}

class TweetModel(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude=['username','like','profile','save_comment']
        # fields='__all__'

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['video']       
