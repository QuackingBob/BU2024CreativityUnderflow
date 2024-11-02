
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from django.contrib.auth.views import LoginView

@login_required
def document_list(request):
    documents = Document.objects.filter(owner=request.user)
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_form.html', {'form': form})



# documents/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            messages.success(request, "Your account has been created successfully!")  # Success message
            return redirect('document_list')  # Redirect to document list or homepage
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "You have logged in successfully!")
        return super().form_valid(form)
