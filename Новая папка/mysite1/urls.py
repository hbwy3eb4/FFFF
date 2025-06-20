"""
URL configuration for mysite1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import TemplateView
from myapp import views as myapp_views

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('features/', TemplateView.as_view(template_name='features.html'), name='features'),
    path('examples/', TemplateView.as_view(template_name='examples.html'), name='examples'),
    path('pricing/', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('blog/', TemplateView.as_view(template_name='blog.html'), name='blog'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('instructions/', TemplateView.as_view(template_name='instructions.html'), name='instructions'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
]

