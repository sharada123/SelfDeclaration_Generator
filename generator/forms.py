from django import forms

# District + Taluka Data (Marathi)
DISTRICT_TALUKA = {
    "पुणे": ["दौंड", "बारामती", "इंदापूर", "शिरूर", "हवेली", "मुळशी", "मावळ", "जुन्नर"],
    "मुंबई": ["मुंबई शहर", "मुंबई उपनगर"],
    "नागपूर": ["नागपूर शहर", "हिंगणा", "काटोल", "कामठी"],
    "नाशिक": ["नाशिक", "सिन्नर", "मालेगाव", "निफाड"],
    "अहमदनगर": ["राहाता", "श्रीरामपूर", "कर्जत", "संगमनेर"]
}

class UserForm(forms.Form):
    name = forms.CharField(label="नाव")
    father_name = forms.CharField(label="वडिलांचे नाव")
    age = forms.CharField(label="वय")
    occupation = forms.CharField(label="व्यवसाय")
    place = forms.CharField(label="गाव")

    # ✅ District Dropdown
    district = forms.ChoiceField(
        label="जिल्हा",
        choices=[(d, d) for d in DISTRICT_TALUKA.keys()]
    )

    # ✅ Taluka Dropdown (initially empty)
    taluka = forms.ChoiceField(
        label="तालुका",
        choices=[]
    )

    mobile = forms.CharField(label="मोबाईल क्रमांक")

    # 🔥 Dynamic Taluka Load
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'district' in self.data:
            district = self.data.get('district')
            talukas = DISTRICT_TALUKA.get(district, [])
            self.fields['taluka'].choices = [(t, t) for t in talukas]
        else:
            self.fields['taluka'].choices = [("", "पहिले जिल्हा निवडा")]