from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# Create your views here.
from .models import buy_lot

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext


from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required








def ok_json(request):
    pass


def error_json(request):
    pass



def transactions(request):
    return render(request, 'trans.html',
                  content_type='text/html')


def dashboard(request):
    return render(request, 'dashboard.html',
                  content_type='text/html')


def registration(request):
    return render(request, 'registration.html',
                  content_type='text/html')


def msg(request):
    return render(request, 'msg.html',
                  content_type='text/html')


def index(request):
    return render(request, 'index.html',
                  content_type='text/html')
