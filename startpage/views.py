from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile
from django.template import RequestContext


from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    return render(request, 'index.html',
                  content_type='text/html')
