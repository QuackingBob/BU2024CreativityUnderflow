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
import documents.views as docviews 
import app.views as appviews
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('documents/', appviews.document_list, name='documents'),  # Ensure this line exists
    path('login/', docviews.CustomLoginView.as_view(), name='login'),  # Adjust according to your project
    path('signup/', docviews.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', docviews.home)
]

# include the app urls
urlpatterns += [
    path('', include('app.urls')),
]


