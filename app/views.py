from django.shortcuts import render
from langchain_demos.constraint_gen import LaTeXGenerator
import cv2
from django.http import HttpResponse, FileResponse, JsonResponse
import os
import subprocess
import re

from .models import Document


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


@login_required
def document_form(request, doc_id=None):
    if doc_id:
        # Load existing document
        document = get_object_or_404(Document, id=doc_id, owner=request.user)
        return render(request, 'app/document_form.html', {'document': document})
    return render(request, 'app/document_form.html')

@login_required
def save_document(request):
    if request.method == 'POST':
        # Get the image data from the request
        image_data = request.FILES.get('image')
        title = request.POST.get('title', 'Untitled')
        latex_content = request.POST.get('latex_content', '')
        
        if 'document_id' in request.POST:
            # Update existing document
            document = get_object_or_404(Document, id=request.POST['document_id'], owner=request.user)
            if image_data:
                document.img_content = image_data
            document.title = title
            document.content = latex_content
        else:
            # Create new document
            document = Document(
                title=title,
                content=latex_content,
                img_content=image_data,
                owner=request.user
            )
        
        document.save()
        return JsonResponse({'success': True, 'document_id': document.id})
    
    return JsonResponse({'success': False}, status=400)

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
    
def create_document(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        img_content = request.FILES['img_content']
        Document.objects.create(title=title, content=content, img_content=img_content, owner=request.user)
        return redirect('document_list')
    return render(request, 'app/document_form.html')

