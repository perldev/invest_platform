
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# Create your views here.
from .models import buy_lot, ClientProfile, InvestDeals,  Accounts, Currency, BankTransfers
from django.conf import settings

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from helpers import http403json, http200json
from django.contrib.auth import login, authenticate, logout


from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Sum
from django.utils import timezone


from django.forms import ModelForm
from django import forms
from decimal import Decimal

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


def auth_logout(request):
    request.session["is_auth"] = False
    request.session["name"] = ""
    logout(request)
    return redirect("/")


def auth_login(request):

    email = request.POST.get("login_email", None)
    pwd = request.POST.get("login_password", None)
    if not pwd or not email:
        return http403json(request)

    username = None
    try:
        u = User.objects.get(email=email)
        username = u.username
    except :
        return http403json(request)

    user = authenticate(username=username, password=pwd)
    if user is not None:
        # A backend authenticated the credentials
        login(request, user)
    else:
        return http403json(request)

    request.session["is_auth"] = True
    return http200json(request, {"status": True,
                                 "username": user.username,
                                 "first_name": user.first_name,
                                 "last_name":  user.last_name})


@login_required
def deposit(request):
    return render(request, 'deposit.html',
                  content_type='text/html')


@login_required
def invoice_create(request):
    context = {}
    for i in  request.POST:
        context[i] = request.POST.get(i)

    context["TO"] = settings.COMPANY_NAME
    context["TO_TAXID"] = settings.COMPANY_TAXID
    context["TO_REGID"] = settings.COMPANY_REGID
    context["TO_COUNTRY"] = settings.COMPANY_COUNTRY
    context["TO_CITY"] = settings.COMPANY_CITY
    context["TO_ADDR"] = settings.COMPANY_ADDR
    context["TO_BANK"] = settings.COMPANY_BANK
    context["TO_ACC"] = settings.COMPANY_ACC
    currency = Currency.objects.get(id=request.POST.get("currency"))
    transfer = BankTransfers(client=request.user,
                             currency=currency,
                             amnt=Decimal(request.POST.get("amnt")),
                             from_bank=settings.COMPANY_BANK,
                             from_account=settings.COMPANY_ACC,
                             )
    transfer.save()
    context["id"] = transfer.id
    context["date"] = transfer.pub_date

    context["currency"] = currency.short_title
    return render(request, 'invoice_template.html', context=context,
                  content_type='text/html')


@login_required
def invoice(request, invoice):
    context = {}
    return render(request, 'invoice_template.html', context=context,
                  content_type='text/html')


@login_required
def transactions(request):
    return render(request, 'trans.html',
                  content_type='text/html')


@login_required
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
    q_obj = InvestDeals.objects.filter(Q(status="created")|Q(status="processing")).values("status").annotate(dsum=Sum("lot__amount")).order_by()
    di = dict([ (i["status"],i["dsum"]) for i in q_obj])
    context = {"lots_buyed": di["processing"],
               "lots_free":di["created"] }

    ub_date__lte=datetime.date.today()
               
    deals = InvestDeals.objects.filter(status="processing", ).values("owner__username",
                                                                   "owner_id").annotate(dcount=Count("owner_id"),
                                                                                        dsum=Sum("lot__amount")        
                                                                   ).order_by()

    deals_repay = InvestDeals.objects.filter(status="processed", ).values("owner__username",
                                                                   "owner_id").annotate(dcount=Count("owner_id"),
                                                                                        dsum=Sum("lot__amount")
                                                                   ).order_by()
                
               
    
    return render(request, 'index.html',
                  context=context,
                  content_type='text/html')


class Client(object):

    def __init__(self, *args, **kwargs):
        self.__user = kwargs["user"]

    def get_balance(self):
        user = self.__user
        acc = Accounts.objects.get(client = user, currency_id=settings.DEFAULT_CURRENCY)
        return acc.balance


    def get_currency(self):
        cur = Currency.objects.get(id=settings.DEFAULT_CURRENCY)
        return cur.short_title



def context_processor(request):
    greed_msg = ""
    if request.user.is_authenticated() :
        greed_msg = "Hello, %s" % request.user.username
        client = Client(user=request.user)
        return {"greed_msg": greed_msg,
                "client": client
               }

    return {}
