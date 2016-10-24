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
from django.views.static import serve
from api.views import LotsToBuy, MyLots, Balance, BuyLot, MyTrans,\
    MyInvoices, CreateWithdraw, LotInfo, CashFlowInfo, CashFlowInfoLot
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.views import login
from django.contrib.auth.views import logout


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'lots': reverse('lots-list', request=request),
        "work_flow": reverse("work_flow", request=request)
    })

urlpatterns = [
    url(r'^api/$', api_root),
    url(r'^api/trans$', MyTrans.as_view(), name='trans'),
    url(r'^api/create/withdraw$', CreateWithdraw.as_view(), name='create-wirthdraw'),
    url(r'^api/invoices/', MyInvoices.as_view(), name='invoices'),
    url(r'^api/lot/([\d]+)$', LotInfo.as_view(), name='lot-info'),
    url(r'^api/lots$', LotsToBuy.as_view(), name='lots-list'),
    url(r'^api/work_flow$', CashFlowInfo.as_view(), name='work_flow'),
    url(r'^api/work_flow/([\d]+)$', CashFlowInfoLot.as_view(), name='work_flow_lot'),
    url(r'^api/my_lots$', MyLots.as_view(), name='user_lots'),
    url(r'^api/buy_lot/([\d]+)$', BuyLot.as_view(), name='buy_lot'),
    url(r'^api/balance$', Balance.as_view(), name='user_balance'),
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('startpage.urls')),

]
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
