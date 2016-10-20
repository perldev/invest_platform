from rest_framework import serializers
from startpage.models import Trans, BankTransfers
from django.contrib.auth.models import User
from rest_framework import serializers


class TransSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trans
        fields = ('id', 'balance1', 'balance2',
                  'res_balance1', 'res_balance2', 'user1_id', 'user2_id',
                  'currency_id', 'amnt', 'status', 'pub_date')


class BankTransfersSerializer(serializers.ModelSerializer):


    class Meta:
        model = BankTransfers
        fields = ('id','from_bank', "name", "country", "city", "address", 'from_account', 'client',
                  'description', 'currency', 'amnt', 'user_accomplished',
                  'pub_date', 'processed_pub_date', 'status', 'debit_credit')
