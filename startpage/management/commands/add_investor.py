from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from startpage.models import Currency, Accounts

from django.db import transaction
from django.utils.timezone import now

import sys

#  the Class lot of investments
"""
class InvestLot(models.Model):
    name = models.CharField(max_length=255, verbose_name="name of Lot")
    amount = models.DecimalField(default="0.0", max_digits=10,
                                 decimal_places=4,
                                 verbose_name="Sum of lot to buy")

    currency = models.ForeignKey(Currency, verbose_name="currency")

    percent = models.DecimalField(default="0.0", max_digits=10, decimal_places=4,
                                  max_length=40, verbose_name="Percent objections on year")
    working_days = models.IntegerField()

    class Meta:
        verbose_name = u'Lot of investments'
        verbose_name_plural = u'Lots of investments'
        ordering = ('-id',)

    def __unicode__(self):
        return self.name
"""

class Command(BaseCommand):
    help = 'create new investor'

    def add_arguments(self, parser):
        parser.add_argument('--investor_first_name', nargs='+', type=str, help='first name',)
        parser.add_argument('--investor_last_name', nargs='+', type=str, help='last name',)
        parser.add_argument('--investor_email', nargs='+', type=str, help='email')
        parser.add_argument('--investor_username', nargs='+', type=str, help='user name')

        parser.add_argument('--investor_pwd', nargs='+', type=str, help="pwd")

    @transaction.atomic
    def handle(self, *args, **options):
        today = now()
        print "today is %s" % today
        first_name = options['investor_first_name'][0]
        last_name = options["investor_last_name"][0]
        email = options["investor_email"][0]
        username = options['investor_username'][0]
        pwd = options['investor_pwd'][0]

        user = User.objects.create_user(username, email, pwd)
        user.first_name = first_name
        user.last_name = last_name

        user.save()
        for i in Currency.objects.all():
            Accounts(client=user, currency=i).save()



