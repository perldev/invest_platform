# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings

from django.db import models
from django.contrib import admin
from django.utils import timezone
from datetime import date, timedelta as td, datetime


DEBIT_CREDIT = (
    ("in", "debit"),
    ("out", "credit")
)

STATUS_ORDER = (
    ("created", u"создан"),
    ("processing", u'в работе'),
    ("processed", u'обработан'),
    ("invest", u'проинвестирован'),
    ("payin", u'пополнение'),
    ("withdraw", u'вывод средств'),
    ("refund", u'закрытие сделки'),
    ("deal", "сделка"),
    ("canceled", u'отменен'),
)


# client profile
class ClientProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"First name&Last name", null=True, blank=True, )
    email = models.CharField(max_length=255, verbose_name=u"Email", null=True, blank=True, )
    phone = models.CharField(max_length=255, verbose_name=u"Phone", null=True, blank=True, )
    nation = models.CharField(max_length=255, verbose_name=u"Nation", null=True, blank=True, )
    birthday = models.DateField(auto_now_add=False, verbose_name=u"Birthday")
    user = models.ForeignKey(User, null=True, blank=True)


# currency
class Currency(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Long title", null=True, blank=True, )
    short_title = models.CharField(max_length=5, verbose_name=u"title", null=True, blank=True, )

    def __unicode__(self):
        return str(self.short_title)



class Bank(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Long title", null=True, blank=True, )
    short_title = models.CharField(max_length=5, verbose_name=u"title", null=True, blank=True, )

    def __unicode__(self):
        return str(self.short_title)


class TransError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


#  the Class lot of investments
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


class InvestDealsAdmin(admin.ModelAdmin):
    list_display = ["id", 'emission_date', 'start_date', 'finish_date',
                    'status', "owner",
                    'admount_refund',
                    ]

    list_filter = ('status', 'owner')
    search_fields = ['^owner__username', '^status']


# invest deal
class InvestDeals(models.Model):

    lot = models.ForeignKey(InvestLot)
    emission_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    finish_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created')

    owner = models.ForeignKey(User, blank=True, null=True)

    buy_trans = models.ForeignKey('Trans',
                                  related_name="trans_buy",
                                  blank=True, null=True)
    refund_trans = models.ForeignKey('Trans',
                                     related_name="trans_refund",
                                     blank=True, null=True)

    admount_refund = models.DecimalField(default="0.0",
                                         max_digits=10,
                                         decimal_places=4,
                                         verbose_name="Amount of refund",
                                         blank=True,
                                         null=True)

    @property
    def currency(self):
        return self.lot.currency

    @property
    def amount(self):
        return self.lot.amount

    class Meta:
        verbose_name = u'Deal'
        verbose_name_plural = u'Deals'
        ordering = ('-id',)


@transaction.atomic
def add_trans(from_acc, amnt, currency, to_acc, status="insufficient_funds", strict=True):

    trans = Trans(balance1=from_acc.balance,
                  balance2=to_acc.balance,
                  user1=from_acc,
                  user2=to_acc,
                  currency=currency,
                  amnt=amnt,
                  status=status)

    if from_acc.currency <> currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core")

    if to_acc.currency <> currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core")

    from_balance = from_acc.balance
    to_new_balance_balance = to_acc.balance
    new_balance = from_balance - amnt
    to_new_balance_balance = to_new_balance_balance + amnt

    if strict:
        if new_balance < 0:
            trans.status = "insufficient_funds"
            trans.save()
            raise TransError("insufficient_funds")

    try:
        with transaction.atomic():
            from_acc.balance = new_balance
            to_acc.balance = to_new_balance_balance
            trans.res_balance1 = new_balance
            trans.res_balance2 = to_new_balance_balance
            trans.save()
            to_acc.save()
            from_acc.save()
            return trans
    except Exception as e:
        trans.status = "core_error"
        trans.save()
        raise TransError("core_error")


class BankTransfers(models.Model):
    from_bank = models.CharField(max_length=255, verbose_name=u"from bank")
    from_account = models.CharField(max_length=255, verbose_name=u"from account")
    client = models.ForeignKey(User, verbose_name=u"Клиент", null=True)
    description = models.CharField(max_length=255, verbose_name=u"Описание", blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=u"Имя получателя", blank=True, null=True)
    country = models.CharField(max_length=255, verbose_name=u"Страна", blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name=u"Город", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=u"Адресс", blank=True, null=True)
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    amnt = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u"Сумма")

    user_accomplished = models.ForeignKey(User, verbose_name=u"Manager",
                                          related_name="operator_processed",
                                          blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата")




    processed_pub_date = models.DateTimeField(auto_now_add=False, verbose_name=u"Дата проводки", null=True)
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created')

    debit_credit = models.CharField(max_length=40,
                                    choices=DEBIT_CREDIT,
                                    default='in')

    class Meta:
        verbose_name = u'Bank transfer'
        verbose_name_plural = u'Bank transfers'

    ordering = ('id',)

    def __unicode__(self):
        return str(self.id) + " " + str(self.amnt) + " " + self.currency.title


@transaction.atomic
def process_bank_acc(bank_transfer, user):
    bank_transfer = BankTransfers.objects.get(id=bank_transfer, status="created", debit_credit="in")
    acc_to = Accounts.objects.get(client=bank_transfer.client, currency=bank_transfer.currency)
    acc_from = Accounts.objects.get(id=settings.BANK_ACCOUNT, currency=bank_transfer.currency)
    add_trans(acc_from, bank_transfer.amnt, bank_transfer.currency, acc_to, "payin", False)
    bank_transfer.status = "processed"
    now = timezone.now()

    bank_transfer.processed_pub_date = now()

    bank_transfer.user_accomplished = user
    bank_transfer.save()
    return True


def accept_transfer(modeladmin, request, queryset):
    for transfer in queryset:
        if transfer.debit_credit == "in":
            process_bank_acc(transfer.id, request.user)

        if transfer.debit_credit == "out":
            transfer.status = "processed"
            now = timezone.now()
            transfer.processed_pub_date = now
            transfer.user_accomplished = request.user
            transfer.save()

accept_transfer.short_description = "Mark selected invoices as received"


# TODO banks account
class BankTransfersAdmin(admin.ModelAdmin):
    list_display = ["id", 'client', 'from_bank', 'from_account',
                    'description', "debit_credit",
                    'amnt', 'currency',
                    'status', "user_accomplished"]

    search_fields = ['^from_account',  '^description', '=amnt', '^user__username', '^status']

    exclude = ("user_accomplished",)

    actions = [accept_transfer]

    fields = ('from_bank', 'from_account', 'processed_pub_date', 'description',
              'status', 'amnt', 'currency')

    def __init__(self, *args, **kwargs):
        super(BankTransfersAdmin, self).__init__(*args, **kwargs)

    def save_model_(self, request, obj, form, change):
        return True


# Create your models here.
class Accounts(models.Model):
    client = models.ForeignKey(User)
    currency = models.ForeignKey("Currency", verbose_name=u"Currency")
    balance = models.DecimalField(verbose_name=u"Getting funds", default=0, max_digits=20, decimal_places=10)
    last_trans_id = models.IntegerField(verbose_name="last_trans", null=True)

    class Meta:
        verbose_name = u'Account in system'
        verbose_name_plural = u'Accounts in system'
        ordering = ('id',)

    def __unicode__(self):
        return "%s %s(%s %s)" % (self.client.first_name, self.client.last_name,
                                 str(self.balance), str(self.currency))


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'currency', 'balance']
    actions = ["add", "delete", "edit"]
    search_fields = ['^client__first_name', '^client__last_name']

    def __init__(self, *args, **kwargs):
        super(AccountsAdmin, self).__init__(*args, **kwargs)


class Trans(models.Model):
    balance1 = models.DecimalField(max_digits=20, editable=False,
                                   decimal_places=10, verbose_name=u"Баланс отправителя")
    balance2 = models.DecimalField(max_digits=20, editable=False,
                                   decimal_places=10, verbose_name=u"Баланс получателя")

    res_balance1 = models.DecimalField(max_digits=20, editable=False, decimal_places=10,
                                       verbose_name=u"Баланс отправителя", null=True)
    res_balance2 = models.DecimalField(max_digits=20, editable=False, decimal_places=10,
                                       verbose_name=u"Баланс получателя", null=True)
    user1 = models.ForeignKey(Accounts, related_name="from_account",
                              verbose_name="Счет отправителя")
    user2 = models.ForeignKey(Accounts, related_name="to_account",
                              verbose_name="Счет получателя")
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")

    amnt = models.DecimalField(max_digits=20, decimal_places=10, verbose_name=u"Сумма")

    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', verbose_name=u"Статус")

    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name=u"Дата",
                                    editable=False)

    class Meta:
        verbose_name = u'Raw transaction'
        verbose_name_plural = u'Raw transactions'
        ordering = ('-id',)

    def __unicode__(self):
        return str(self.id)


def cancel_trans(modeladmin, request, queryset):

    for i in queryset:
        add_trans(i.user2, i.amnt, i.currency, i.user1, "revert", False)

cancel_trans.short_description = "Cancel transaction"


class TransAdmin(admin.ModelAdmin):
    list_display = ['id', 'user1', 'balance1', 'user2', 'balance2', 'currency', 'amnt', 'status',
                    'res_balance1', 'res_balance2', 'pub_date']
    list_filter = ('status', 'currency')

    actions = ["add", cancel_trans]

    def __init__(self, *args, **kwargs):
        super(TransAdmin, self).__init__(*args, **kwargs)


@transaction.atomic
def buy_lot(type_of_lot, user):

    deal = InvestDeals.objects.filter(status="created", lot_id=type_of_lot).order_by('id').first()
    if not deal:
        raise TransError("there is no lot for sale")
    # TODO add currency exchange
    lot = deal.lot
    acc_from = Accounts.objects.get(client=user,
                                    currency=lot.currency)
    acc_to = Accounts.objects.get(id=settings.INVESTMENT_ACCOUNT,
                                  currency=lot.currency)
    trans = add_trans(acc_from, lot.amount, lot.currency, acc_to, "deal", True)

    now = timezone.now()
    deal.start_date = now
    deal.finish_date = now + td(days=lot.working_days)
    deal.status = "processing"
    deal.owner = user
    deal.buy_trans = trans
    deal.admount_refund = lot.amount*(1+lot.percent/100)
    deal.save()

    return True


