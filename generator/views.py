from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import UserForm
from datetime import date


def generate_pdf(request):

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

            HTML(string=html).write_pdf(response)

            return response

        return render(request, 'form.html', {'form': form})
def to_marathi_number(number):
    eng = "0123456789"
    mar = "०१२३४५६७८९"
    return str(number).translate(str.maketrans(eng, mar))