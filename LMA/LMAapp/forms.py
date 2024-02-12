from django import forms
from .models import Add_Bag,User_details

class AddBagForm(forms.ModelForm):
    class Meta:
        model = Add_Bag
        fields = [ 'UserName' , 'Book_Title']

