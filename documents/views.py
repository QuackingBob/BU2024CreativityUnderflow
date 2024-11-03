
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from django.contrib.auth.views import LoginView


@login_required
def profile(request):
    # Pass the user's name in the context
    form = DocumentForm()
    return render(request, 'user/profile.html', {'form': form, 'username': request.user.username})


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
            return redirect('/documents')  # Redirect to document list or homepage
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "You have logged in successfully!")
        # Use the next parameter for redirection
        return super().form_valid(form)
    

def home(request):
    form=  DocumentForm()
    return render(request, 'app/home.html')