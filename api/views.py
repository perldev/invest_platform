from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import *
from startpage.models import InvestDeals, buy_lot, TransError, Accounts

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from decimal import Decimal
from django.db.models import Q
from rest_framework import filters
from django.db.models import Count

class LotsToBuy(APIView):
    """
    A custom endpoint for GET request.
    """

    def get(self, request, format=None):
        """
        Return a hardcoded response.
        """
        deals = InvestDeals.objects.filter(status="created").values("lot__amount","lot__percent",
                                                                    "lot__working_days",
                                                                    "lot__percent",
                                                                    "lot__name",
                                                                    "lot_id").annotate(dcount=Count("lot_id")).order_by()

        return Response({"success": True,
                         "deals2buy": deals})


class MyLots(APIView):
    """
    A custom endpoint for GET request.
    """

    def get(self, request, format=None):
        """
        Return a hardcoded response.
        """
        deals = InvestDeals.objects.filter(status="processing",
                                           owner=request.user).values("lot__amount",
                                                                      "lot__percent",
                                                                      "lot__working_days",
                                                                      "lot__percent",
                                                                      "lot__name",
                                                                      "lot_id").annotate(dcount=Count("lot_id")).order_by()
        return Response({"success": True,
                         "deals": deals})


class BuyLot(APIView):
    """
    A custom endpoint for GET request.
    """
    def get(self, request, lot_id, format=None):
        """
        Return a hardcoded response.
        """
        try:
            buy_lot(lot_id, request.user)
            return Response({"success": True })
        except TransError as e:
            return Response({"success": False, "description": e.message})


class Balance(APIView):
    """
    A custom endpoint for GET request.
    """

    def get(self, request, format=None):
        """
        Return a hardcoded response.
        """
        res = {}
        for i in Accounts.objects.filter(client = request.user):
            res[i.currency.short_title] = i.balance
        res["status"] = True
        return Response(res)



class MyTrans(generics.ListAPIView):
    """
        Get transes for one user

    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^amnt', 'id' )
    model = Trans
    serializer_class = TransSerializer

    def get_queryset(self):
        user = self.request.user
        list_q1=[]
        for acc in   Accounts.objects.filter(client = user):
            list_q1.append(Q(user1=acc))
            list_q1.append(Q(user2=acc))

        query = list_q1.pop()
        for q in list_q1:
            query |= q

        return Trans.objects.filter(q)


