from rest_framework import serializers
from startpage.models import Trans
from django.contrib.auth.models import User
from rest_framework import serializers


class TransSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trans
        fields = ('id', 'balance1', 'balance2',
                  'res_balance1', 'res_balance2', 'user1_id', 'user2_id',
                  'currency_id', 'amnt', 'status', 'pub_date')
