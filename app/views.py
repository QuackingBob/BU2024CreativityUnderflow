from django.shortcuts import render
from langchain_demos.constraint_gen import LaTeXGenerator
import cv2
from django.http import HttpResponse, FileResponse
import os
import subprocess
import re


from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.contrib.auth.decorators import login_required

@login_required
def document_list(request):
    if request.user.is_authenticated:
        # Get documents that belong to the logged-in user
        documents = Document.objects.filter(owner=request.user)
        print(len(documents))
        print(f'username: {request.user}')
    else:
        # Option 1: Redirect unauthenticated users to the login page
        return redirect('login')
    return render(request, 'app/document_list.html', {'app': documents})

@login_required
def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)
    return render(request, 'app/document_detail.html', {'app': document})



def document_form(request):
    return render(request, 'app/document_form.html')


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
