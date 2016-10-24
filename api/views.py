from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import *
from startpage.models import InvestDeals, buy_lot, TransError, Accounts, BankTransfers, add_trans, InvestLot
from django.db import models
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from decimal import Decimal
from django.db.models import Q
from rest_framework import filters
from django.db.models import Count
from django.utils import timezone

MONTH = ["",
'Jan',
'Feb',
'Mar',
'Apr',
'May',
'Jun',
'Jul',
'Aug',
'Sep',
'Oct',
'Nov',
'Dec'
]

class CashFlowInfoLot(APIView):
    
     def get(self, request, pk, format=None):

        user = request.user

        now = timezone.now()
        year = now.year

        # adding year objections
        lot = InvestLot.objects.get(id=pk)
        q_obj = Q(owner=user) & Q(start_date__year=year) & Q(status="processed")
        q_obj = InvestDeals.objects.filter(q_obj).order_by("id")

        result = dict([(MONTH[i], {"invest":0,
                                   "refund_investments": 0,
                                   "wait_income": 0
                                   }) for i in range(1, 13)])
        
        current_month = None
        current_addit = {}
        for trans in q_obj:
            dtime = trans.start_date
            dtime1 = trans.finish_date
            result[MONTH[dtime.month]]["invest"] += lot.amount
            if dtime1.year == year:
                result[MONTH[dtime1.month]]["refund_investments"] += trans.admount_refund
                
        q_obj = Q(owner=user) & Q(start_date__year=year) & Q(status="processing")
        for trans in InvestDeals.objects.filter(q_obj).order_by("id"):
            dtime = trans.start_date
            dtime1 = trans.finish_date
            result[MONTH[dtime.month]]["invest"] += lot.amount
            if dtime1.year == year:
                result[MONTH[dtime1.month]]["wait_income"] += trans.admount_refund
            continue

        return Response({"lot": {"title": lot.name, "id": lot.id},
                         "categories": MONTH[1:], "result": result})


class CashFlowInfo(APIView):

    def get(self, request, format=None):

        user = request.user
        list_q1 = []
        for acc in Accounts.objects.filter(client=user):
            list_q1.append(Q(user1=acc))
            list_q1.append(Q(user2=acc))
        query = list_q1.pop()
        # gather all accounts of client
        for q in list_q1:
            query |= q

        now = timezone.now()
        year = now.year

        # adding year objections


        q_obj = Trans.objects.filter((query) & Q(pub_date__year=year)).order_by("id")
        result_month = dict([(MONTH[i], {"invest": 0,
                                         "refund_investments": 0,
                                         "wait_income": 0,
                                         "cashin": 0,
                                         "cashout": 0,
                                        }) for i in range(1, 13)])

        current_month = None
        current_addit = {}
        for trans in q_obj:
            dtime = trans.pub_date
            if dtime.month != current_month:
                if current_month is not None:
                    result_month[current_addit["month"]] = current_addit

                current_month = dtime.month
                current_addit = {"cashin":0,
                                 "cashout":0,
                                 "invest":0,
                                 "refund_investments":0,
                                 "wait_income": 0,
                                 "month": MONTH[dtime.month]}

            if trans.status == "deal":
                current_addit["invest"] += trans.amnt
                continue

            if trans.status == "withdraw":
                current_addit["cashout"] += trans.amnt
                continue

            if trans.status == "payin":
                current_addit["cashin"] += trans.amnt
                continue

            if trans.status == "refund":
                current_addit["refund_investments"] += trans.amnt
                continue

        q_obj = Q(owner=user) & Q(finish_date__year=year) & Q(status="processing")

        for trans in InvestDeals.objects.filter(q_obj).order_by("id"):
            dtime = trans.finish_date
            if dtime.month != current_month:
                if current_month is not None:
                    result_month[current_addit["month"]] = current_addit

                current_month = dtime.month
                current_addit = {"cashin": 0,
                                 "cashout": 0,
                                 "invest": 0,
                                 "refund_investments": 0,
                                 "wait_income": 0,
                                 "month": MONTH[dtime.month]}

            current_addit["wait_income"] += trans.admount_refund
            continue

        if "month" in current_addit:
            result_month[current_addit["month"]] = current_addit

        return Response({"categories": MONTH[1:], "result": result_month})


class LotInfo(APIView):

    def get(self, request, pk, format=None):
        lot = InvestLot.objects.get(id=pk)
        return Response({"lot_info": LotSerializer(lot).data, "status": True})


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


class MyInvoices(generics.ListAPIView):
    """
        Get transes for one user

    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^amnt', '^status' )
    model = BankTransfers
    serializer_class = BankTransfersSerializer
    ordering = ('-id',)

    def get_queryset(self):
        user = self.request.user
        return BankTransfers.objects.filter(client=user)


class CreateWithdraw(generics.CreateAPIView):

    model = BankTransfers

    def post(self, request):

        serializer = BankTransfersSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'status': False}, status=500)

        bank_transfer = serializer.save(client=self.request.user,
                                        pub_date=timezone.now(),
                                        debit_credit="out",
                                        status="processing")
        acc_from = Accounts.objects.get(client=bank_transfer.client, currency=bank_transfer.currency)
        acc_to = Accounts.objects.get(id=settings.BANK_ACCOUNT, currency=bank_transfer.currency)
        add_trans(acc_from, bank_transfer.amnt, bank_transfer.currency, acc_to, "withdraw", True)
        return Response({"status": True}, status=200)


class MyTrans(generics.ListAPIView):
    """
        Get transes for one user

    """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^amnt', 'id' )
    model = Trans
    serializer_class = UserTransSerializer
    ordering = ('-id',)

    def __init__(self, *args, **kwargs):
        self.__accounts = None
        super(MyTrans, self).__init__(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['accounts'] = self.__accounts
        return serializer_class(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.__accounts = [i.id for i in Accounts.objects.filter(client=self.request.user)]
        return super(MyTrans, self).get(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        list_q1=[]
        for acc in Accounts.objects.filter(client=user):
            list_q1.append(Q(user1=acc))
            list_q1.append(Q(user2=acc))

        query = list_q1.pop()
        for q in list_q1:
            query |= q

        q_obj = Trans.objects.filter(query)
        return q_obj


