from django import forms
from .models import SolderPost, MainUser

# class SolderForm(forms.Form):
#     first_name = forms.CharField(max_length=150)
#     middle_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     desc = forms.CharField(widget=forms.Textarea)
#     birth_date = forms.DateField()
#     Death_date = forms.DateField()
#     is_alive = forms.BooleanField()
#     photo = forms.ImageField()
    
class SolderForm(forms.ModelForm):
    class Meta:
        model = SolderPost
        fields = ['first_name', 'middle_name', 'last_name', 'desc', 'is_alive', 'photo', 'birth_date', 'death_date']


    def test(self):
        return self.cleaned_data["death_date"]
# , "birth_date", "death_date"