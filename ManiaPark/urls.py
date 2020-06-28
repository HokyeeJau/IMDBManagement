"""ManiaPark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views
from . import connect_db
urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main, name='main'),
    path('main/actor/', views.actor, name='actor'),
    path('main/director/', views.director, name='director'),
    path('main/movie/', views.movie, name='movie'),

    path('main/actor/asearch', views.filter_actor, name='asearch'),
    path('main/actor/aedit', views.edit_actor, name='aedit'),
    path('main/actor/adelete', views.delete_actor, name='adelete'),
    path('main/actor/amodify', views.modify_actor, name='amodify'),
    path('main/actor/add', views.add_apointer, name='add'),
    path('main/actor/aadd', views.add_actor, name='aadd'),

    path('main/director/dsearch', views.filter_director, name='dsearch'),
    path('main/director/dedit', views.edit_director, name='dedit'),
    path('main/director/ddelete', views.delete_director, name='ddelete'),
    path('main/director/dmodify', views.modify_director, name='dmodify'),
    path('main/director/dadd', views.add_dpointer, name='dadd'),
    path('main/director/ddadd', views.add_director, name='ddadd'),

    path('main/movie/msearch', views.filter_movie, name='msearch'),
    path('main/movie/medit', views.edit_movie, name='medit'),
    path('main/movie/mdelete', views.delete_movie, name='mdelete'),
    path('main/movie/mmodify', views.modify_movie, name='mmodify'),
    path('main/movie/madd', views.add_mpointer, name='madd'),
    path('main/movie/mmadd', views.add_movie, name='mmadd'),

]
