from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
import os

from weasyprint import HTML, CSS
from .forms import UserForm
from .utils import get_fonts


# ---------- Helpers ----------
def file_url(path):
    return "file://" + path.replace("\\", "/")


def to_marathi_number(number):
    eng = "0123456789"
    mar = "०१२३४५६७८९"
    return str(number).translate(str.maketrans(eng, mar))


# ---------- Fonts ----------
fonts = get_fonts()

font_regular = file_url(fonts["regular"])
font_bold = file_url(fonts["bold"])
font_dejavu = file_url(fonts["dejavu"])


def generate_pdf(request):

    # logo path (SAFE)
    logo_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'logo.png'))
    print(logo_path)
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'form.html', {'form': form})

    form = UserForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        # Marathi numbers
        data['mobile'] = to_marathi_number(data.get('mobile', ''))
        data['age'] = to_marathi_number(data.get('age', ''))

        # date
        today = date.today().strftime("%d/%m/%Y")
        data['today'] = to_marathi_number(today)

        # assets
        data['logo_path'] = logo_path

        # render HTML
        html_string = render_to_string('pdf_template.html', data)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        HTML(string=html_string).write_pdf(
            response,
            stylesheets=[
                CSS(string=f"""
                @font-face {{
                    font-family: 'Marathi';
                    src: url('{font_regular}');
                    font-weight: normal;
                }}

                @font-face {{
                    font-family: 'Marathi';
                    src: url('{font_bold}');
                    font-weight: bold;
                }}

                @font-face {{
                    font-family: 'NumberFont';
                    src: url('{font_dejavu}');
                }}

                body {{
                    font-family: 'Marathi', sans-serif;
                }}

                .num {{
                    font-family: 'NumberFont';
                }}

                b, strong {{
                    font-weight: bold;
                }}
                """)
            ]
        )

        return response

    return render(request, 'form.html', {'form': form})