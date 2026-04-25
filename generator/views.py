from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from datetime import date
import os

from weasyprint import HTML, CSS
from .forms import UserForm


# ---------- Helper ----------
def file_url(path):
    return "file://" + path.replace("\\", "/")


def to_marathi_number(number):
    eng = "0123456789"
    mar = "०१२३४५६७८९"
    return str(number).translate(str.maketrans(eng, mar))


# ---------- MAIN VIEW ----------
def generate_pdf(request):

    if request.method == 'GET':
        form = UserForm()
        return render(request, 'form.html', {'form': form})

    form = UserForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        # Marathi numbers
        data['mobile'] = to_marathi_number(data.get('mobile', ''))
        data['age'] = to_marathi_number(data.get('age', ''))

        today = date.today().strftime("%d/%m/%Y")
        data['today'] = to_marathi_number(today)

        # 🔥 LOGO PATH
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'logo', 'logo.png')
        shri_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'shri.png'))
        patr_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'patr.png'))
        kr_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'kr.png'))
        pr_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'pr.png'))
        patra_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'logo', 'patra.png'))
        data['patra_path'] = patra_path
        data['logo_path'] = logo_path
        data['shri_path'] = shri_path
        data['patr_path'] = patr_path
        data['kr_path'] = kr_path
        data['pr_path'] = pr_path
        # 🔥 FONT PATHS (IMPORTANT)
        font_regular = file_url(os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSerifDevanagari-Regular.ttf'))
        font_bold = file_url(os.path.join(settings.BASE_DIR, 'static', 'fonts', 'NotoSerifDevanagari-Bold.ttf'))

        # HTML render
        html_string = render_to_string('pdf_template.html', data)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # 🔥 FINAL PDF GENERATION
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
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

                body {{
                    font-family: 'Marathi';
                    font-feature-settings: "liga" 1;
                    font-variant-ligatures: normal;
                }}

                strong, b {{
                    font-weight: bold;
                }}
                """)
            ]
        )

        return response

    return render(request, 'form.html', {'form': form})