from rest_framework import serializers
from startpage.models import Trans, BankTransfers, InvestLot
from django.contrib.auth.models import User
from rest_framework import serializers


class UserTransSerializer(serializers.ModelSerializer):

    debit_credit = serializers.SerializerMethodField()

    def __init__(self, *args, **kargs):
        self.__accounts = kargs.get("accounts", [])
        del kargs["accounts"]
        super(UserTransSerializer, self).__init__(*args, **kargs)

    class Meta:
        model = Trans
        fields = ('id', 'balance1', 'balance2',
                  'res_balance1', 'res_balance2', 'user1', 'user2',
                  'currency', 'amnt', 'status', 'pub_date', "debit_credit")

    def get_debit_credit(self, obj):
        if obj.user1_id in self.__accounts:
            return "out"

        if obj.user2_id in self.__accounts:
            return "in"

        return "not_set"


class LotSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestLot
        fields = ('id', 'working_days', "percent", "currency", "amount", "name")


class BankTransfersSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankTransfers
        fields = ('id','from_bank', "name", "country", "city", "address", 'from_account', 'client',
                  'description', 'currency', 'amnt', 'user_accomplished',
                  'pub_date', 'processed_pub_date', 'status', 'debit_credit')
