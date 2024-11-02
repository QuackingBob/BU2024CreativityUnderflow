"""AuToTeX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from documents import views 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('documents/', include('documents.urls')),
 #   path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs
 #   path('signup/', views.signup, name='signup'),
    path('documents/', views.document_list, name='document_list'),  # Ensure this line exists
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Adjust according to your project
    path('signup/', views.signup, name='signup'),
     path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 
     
]
