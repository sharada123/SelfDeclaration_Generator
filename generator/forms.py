from django import forms



class UserForm(forms.Form):
    name = forms.CharField(label="नाव")
    father_name = forms.CharField(label="वडिलांचे नाव")
    age = forms.CharField(label="वय")
    occupation = forms.CharField(label="व्यवसाय")
    place = forms.CharField(label="गाव")

    district = forms.CharField(label="जिल्हा")
    taluka = forms.CharField(label="तालुका")

    mobile = forms.CharField(label="मोबाईल क्रमांक")

