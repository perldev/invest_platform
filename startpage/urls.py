"""banksite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from .views import index, dashboard, registration, msg,\
    transactions, regis_confirm, regis_finish, auth_login, auth_logout, deposit,\
    invoice_create




urlpatterns = [
    url(r'^dashboard', dashboard, name="dashboard"),
    url(r'^deposit', deposit, name="deposit"),
    url(r'^invoice/create', invoice_create, name="invoice_create"),
    url(r'^registration', registration, name="registration"),
    url(r'^registration_confirm', regis_confirm, name="regis_confirm"),
    url(r'^registration_finish', regis_finish, name="regis_finish"),
    url(r'^auth_logout', auth_logout, name="auth_logout"),
    url(r'^auth_login', auth_login, name="auth_login"),
    url(r'^msg', msg, name="msg"),
    url(r'^transactions', transactions, name="trans"),
    url(r'^', index, name="index"),
]

