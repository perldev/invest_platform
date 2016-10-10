from django.core.management.base import BaseCommand, CommandError
from startpage.models import InvestLot, Currency, InvestDeals
from django.db import transaction
from django.utils.timezone import now
from decimal import Decimal
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
    help = 'calculate credit'


    def add_arguments(self, parser):
        parser.add_argument('--lot_name', dest='lot_name', nargs=1, type=str, help='name of the lot',)
        parser.add_argument('--lot_duration', dest='lot_duration', nargs=1, type=int, help='durations in the days',)
        parser.add_argument('--lot_amount', dest='lot_amount', nargs=1, type=str, help='amount of each lot')
        parser.add_argument('--lot_currency', dest='lot_currency', nargs=1, type=str, help='currency of the lot')
        parser.add_argument('--lot_percent', dest='lot_percent', nargs=1, type=str, help='percent of the lot')
        parser.add_argument('--lot_count', dest='lot_count', nargs=1, type=int, help='number of the lots')


    @transaction.atomic
    def handle(self, *args, **options):
        today = now()
        print options
        print "today is %s" % today
        count_of_lots = options['lot_count'][0]
        working_days = options["lot_duration"][0]
        lot_percent = Decimal(options["lot_percent"][0])
        lot_name = options['lot_name'][0]
        lot_amount = Decimal(options["lot_amount"][0])
        currency = options["lot_currency"][0]
        try:
            currency = Currency.objects.get(short_title=currency)
        except Currency.DoesNotExist:
            print "currency does not exist %s " % currency
            sys.exit(0)

        print "we will generate %i lots" % count_of_lots
        print "name \"%s\" on %i day with the percent on each one %f" % (lot_name, working_days, lot_percent)
        lot = None
        try:
            lot = InvestLot.objects.get(working_days=working_days,
                                        amount=lot_amount,
                                        currency=currency,
                                        percent=lot_percent)
            print "i have found lot %s " % lot.name
        except InvestLot.DoesNotExist:
            lot = InvestLot(working_days=working_days,
                            name=lot_name,
                            amount=lot_amount,
                            currency=currency,
                            percent=lot_percent
                            )
            lot.save()
            # TODO add ask question for confirm
            print "i have NOT found this  lot %s " % lot.name
            print "i have create this type of lots"

        for i in range(0, count_of_lots):
            InvestDeals(lot=lot).save()

        print "Total: %s" % (lot_amount*count_of_lots)