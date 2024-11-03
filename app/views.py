from django.shortcuts import render
from langchain_demos.constraint_gen import LaTeXGenerator
import cv2
from django.http import HttpResponse, FileResponse
import os
import subprocess
import re

# Create your views here.

def document_form(request):
    return render(request, 'app/document_form.html')


def document_list(request):
    return render(request, 'app/document_list.html')

def render_image(request):
    # get image from request
    image = request.FILES['image']
    # save image to static folder
    with open('static/image.png', 'wb') as f:
        f.write(image.read())
        
    
    generator = LaTeXGenerator()
    img = cv2.imread('static/image.png')
    latex = generator.generate(img)
    latex = re.sub(r'```latex\n', '', latex)
    latex = re.sub(r'```', '', latex)
    with open('static/output.tex', 'w') as f:
        f.write(latex)
    
    # output output.pdf to static folder
    subprocess.run(['pdflatex', '-output-directory=static', 'static/output.tex'])
    pdf_path = 'static/output.pdf'
    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    
    return HttpResponse(status=500)

def get_latex(request):
    try:
        with open('static/output.tex', 'r') as f:
            latex_content = f.read()
        return HttpResponse(latex_content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse(status=404)