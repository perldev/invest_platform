from django.core.management.base import BaseCommand, CommandError
from startpage.models import InvestLot
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
    help = 'calculate credit'


    def add_arguments(self, parser):
        parser.add_argument('lot_name', nargs='+', type=str, help='name of the lot',)
        parser.add_argument('lot_duration', nargs='+', type=int, help='durations in the days',)
        parser.add_argument('lot_percent', nargs='+', type=float, help='percent of the lot')
        parser.add_argument('lot_count', nargs='+', type=int, help='number of the lots')


    @transaction.atomic
    def handle(self, *args, **options):
        today = now()
        print "today is %s" % today
        print "we will generate %i lots" % options['lot_count']
        print "name %s on %i day with the percent on each one %.2d" % (options['lot_name'],
                                                                       options["lot_duration"],
                                                                       options["lot_percent"])


