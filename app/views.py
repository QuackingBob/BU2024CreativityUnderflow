from django.shortcuts import render

# Create your views here.

def document_form(request):
    return render(request, 'app/document_form.html')


def document_list(request):
    return render(request, 'app/document_list.html')

