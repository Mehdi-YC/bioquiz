"""Bioquiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
import rest_framework
from django.conf.urls import url
from . import views

#adding the routes for the app views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^$',views.index,name='home'),
    url('login',views.login,name='login'),
    url('register',views.register,name='register'),
    url('questions/',views.list_Question),
    url('images/',views.get_images),
    url('categories/',views.get_categories),
    url(r'^logout', views.logout_user, name='logout'),
    url(r'^answer', views.check_answer, name='answer'),
]
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
