from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import UserForm
from datetime import date
#added for live site 
from django.conf import settings
import os
from weasyprint import HTML, CSS
from .utils import get_fonts

fonts = get_fonts()

font_regular = fonts["regular"]
font_bold = fonts["bold"]
font_dejavu = fonts["dejavu"]
def generate_pdf(request):
    #font_path = os.path.join(settings.BASE_DIR, "fonts", "NotoSansDevanagari-Regular.ttf")
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'form.html', {'form': form})

    elif request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            # 🔥 Convert to Marathi digits
            data['mobile'] = to_marathi_number(data.get('mobile', ''))
            data['age'] = to_marathi_number(data.get('age', ''))
            
            today = date.today()

            # 🔥 Format: DD/MM/YYYY
            formatted_date = today.strftime("%d/%m/%Y")

            # 🔥 Convert to Marathi digits
            data['today'] = to_marathi_number(formatted_date)

            html = render_to_string('pdf_template.html', data)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="output.pdf"'

            #HTML(string=html).write_pdf(response)
            #added for live
            HTML(string=html).write_pdf(
            response,
            stylesheets=[
            CSS(string=f"""
            @font-face {{
                font-family: 'NotoDev';
                src: url('file://{font_regular}');
            }}

            @font-face {{
                font-family: 'NotoDev';
                src: url('file://{font_bold}');
                font-weight: bold;
            }}

            @font-face {{
                font-family: 'DejaVu';
                src: url('file://{font_dejavu}');
            }}

            body {{
                font-family: 'NotoDev', 'DejaVu', sans-serif;
            }}

            b, strong {{
                font-family: 'NotoDev';
                font-weight: bold;
            }}
        """)
    ]
)
            return response

        return render(request, 'form.html', {'form': form})
def to_marathi_number(number):
    eng = "0123456789"
    mar = "०१२३४५६७८९"
    return str(number).translate(str.maketrans(eng, mar))