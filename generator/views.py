from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from django.conf import settings
from .forms import UserForm


def generate_pdf(request):

    if request.method == 'GET':
        return render(request, 'form.html', {'form': UserForm()})

    form = UserForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        # ---------- FONT ----------
        font_path = os.path.join(settings.BASE_DIR, "static/fonts/NotoSansDevanagari-Regular.ttf")
        pdfmetrics.registerFont(TTFont('Marathi', font_path))

        # ---------- DOCUMENT ----------
        doc = SimpleDocTemplate(response, pagesize=A4)

        # ---------- STYLES ----------
        normal = ParagraphStyle(name='Normal', fontName='Marathi', fontSize=12, leading=16)
        center = ParagraphStyle(name='Center', fontName='Marathi', fontSize=14, alignment=TA_CENTER)
        right = ParagraphStyle(name='Right', fontName='Marathi', fontSize=12, alignment=TA_RIGHT)

        content = []

        # ---------- LOGO ----------
        logo_path = os.path.join(settings.BASE_DIR, "static/logo/logo.png")
        if os.path.exists(logo_path):
            content.append(Image(logo_path, width=120, height=60))

        content.append(Spacer(1, 10))

        # ---------- HEADER ----------
        content.append(Paragraph("संदर्भ शासन निर्णय क्रमांक : प्रसुधा /१६१४ /३४५/प्र.क्र.....७१/१८-अ", normal))
        content.append(Spacer(1, 10))

        # ---------- TITLE ----------
        content.append(Paragraph("प्रपत्र - अ", center))
        content.append(Paragraph("स्वयं घोषणा पत्र", center))
        content.append(Spacer(1, 15))

        # ---------- MAIN TEXT ----------
        text1 = f"""
        मी {data['name']} श्री {data['father_name']} यांचा मुलगा/मुलगी/पत्नी,
        वय {data['age']} वर्ष, व्यवसाय {data['occupation']},
        राहणार {data['place']}, तालुका {data['taluka']}, जिल्हा {data['district']}
        या द्वारे घोषित करतो / करते की, वरील सर्व माहिती माझ्या व्यक्तिगत माहिती व समजुतीनुसार खरी आहे.
        """

        content.append(Paragraph(text1, normal))
        content.append(Spacer(1, 10))

        text2 = """
        सदर माहिती खोटी आढळून आल्यास, भारतीय दंड संहिता १९६० कलम १९९ व २०० व अन्य कायद्यानुसार
        माझ्यावर खटला भरला जाईल व मी शिक्षेस पात्र राहीन.
        """

        content.append(Paragraph(text2, normal))
        content.append(Spacer(1, 20))

        # ---------- DATE ----------
        today = date.today().strftime("%d/%m/%Y")

        content.append(Paragraph("ठिकाण : दौंड", normal))
        content.append(Paragraph(f"दिनांक : {today}", normal))
        content.append(Spacer(1, 20))

        content.append(Paragraph("अर्जदार सही", right))
        content.append(Paragraph(data['name'], right))

        # ---------- SECOND SECTION ----------
        content.append(Spacer(1, 20))

        content.append(Paragraph("प्रपत्र – ब", center))
        content.append(Paragraph("स्वयं-साक्षांकनासाठी स्वयंघोषणा पत्र", center))
        content.append(Spacer(1, 10))

        text3 = f"""
        मी {data['name']} श्री {data['father_name']} यांचा मुलगा/मुलगी/पत्नी,
        वय {data['age']} वर्ष, व्यवसाय {data['occupation']},
        राहणार {data['place']}, तालुका {data['taluka']}, जिल्हा {data['district']}
        या द्वारे घोषित करतो / करते की, स्वयं साक्षांकित केलेल्या प्रती या मूळ कागदपत्रांच्या सत्यप्रती आहेत.
        """

        content.append(Paragraph(text3, normal))
        content.append(Spacer(1, 20))

        content.append(Paragraph(f"मोबाईल क्र.: {data['mobile']}", normal))

        # ---------- PAGE BREAK ----------
        content.append(PageBreak())

        # ---------- PAGE 2 ----------
        content.append(Paragraph("स्वयं घोषणा पत्र", center))
        content.append(Paragraph("(रहिवाशीदाखला - लाभार्थी)", center))
        content.append(Spacer(1, 10))

        text4 = f"""
        मी {data['name']} श्री {data['father_name']} यांचा मुलगा/मुलगी/पत्नी,
        वय {data['age']} वर्ष, व्यवसाय {data['occupation']},
        राहणार {data['place']}, ता. {data['taluka']}, जि. {data['district']}
        या द्वारे घोषित करतो / करते की, वरील माहिती खरी आहे.
        """

        content.append(Paragraph(text4, normal))
        content.append(Spacer(1, 20))

        content.append(Paragraph("अर्जदार सही", right))
        content.append(Paragraph(data['name'], right))

        # ---------- BUILD ----------
        doc.build(content)

        return response

    return render(request, 'form.html', {'form': form})