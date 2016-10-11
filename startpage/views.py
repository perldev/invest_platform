from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# Create your views here.
from .models import buy_lot, ClientProfile

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext


from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

from django.forms import ModelForm
from django import forms

"""
name = models.CharField(max_length=255, verbose_name=u"First name&Last name", null=True, blank=True, )
email = models.CharField(max_length=255, verbose_name=u"Email", null=True, blank=True, )
phone = models.CharField(max_length=255, verbose_name=u"Phone", null=True, blank=True, )
nation = models.CharField(max_length=255, verbose_name=u"Nation", null=True, blank=True, )
birthday = models.DateField(auto_now_add=False, verbose_name=u"Birthday")
user = models.ForeignKey(User)
"""

class ClientForm(ModelForm):

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        if "fred@example.com" not in data:
            raise forms.ValidationError("You have forgotten about Fred!")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    class Meta:
         model = ClientProfile
         fields = ['name', 'email', 'phone', 'nation', "birthday"]



def transactions(request):
    return render(request, 'trans.html',
                  content_type='text/html')


def dashboard(request):
    return render(request, 'dashboard.html',
                  content_type='text/html')


def registration(request):
    return render(request, 'registration.html',
                  content_type='text/html')



def regis_confirm(request):

    f = ClientForm(request.POST)
    if f.is_valid():
        f.save()


def regis_finish(request):
    pass


def msg(request):
    return render(request, 'msg.html',
                  content_type='text/html')


def index(request):
    return render(request, 'index.html',
                  content_type='text/html')
