from django.shortcuts import render
from langchain_demos.constraint_gen import LaTeXGenerator
import cv2
from django.http import HttpResponse, FileResponse, JsonResponse
import os
import subprocess
import re
from .forms import DocumentForm
from .models import Document


from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class DocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        """
        Optionally restricts the returned documents to the owner,
        by filtering against the authenticated user.
        """
        user = self.request.user
        return Document.objects.filter(owner=user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Associates the document with the authenticated user.
        """
        serializer.save(owner=self.request.user)
        
    
    @action(detail=False, methods=['post'], url_path='save_document')
    def save_document(self, request):
        """
        Custom action to handle saving a document with image upload.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({'success': True, 'document_id': serializer.instance.id})
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=400)

@login_required
def document_detail(request, document_id):
    """
    Display a specific document based on its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        document_id (int): The ID of the document to display.

    Returns:
        HttpResponse: Renders the document_form.html template with the document context.
    """
    # Retrieve the document ensuring it belongs to the logged-in user
    document = get_object_or_404(Document, id=document_id, owner=request.user)
    
    # Render the template with the document context
    return render(request, 'app/document_form.html', {'document': document})

def document_list(request):
    documents = Document.objects.filter(owner=request.user)
    return render(request, 'app/document_list.html', {'documents': documents})

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

