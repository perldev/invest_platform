# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-10 13:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=10, default=0, max_digits=20, verbose_name='Getting funds')),
                ('last_trans_id', models.IntegerField(null=True, verbose_name='last_trans')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Account in system',
                'verbose_name_plural': 'Accounts in system',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Long title')),
                ('short_title', models.CharField(blank=True, max_length=5, null=True, verbose_name='title')),
            ],
        ),
        migrations.CreateModel(
            name='BankTransfers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_bank', models.CharField(max_length=255, verbose_name='from account')),
                ('from_account', models.CharField(max_length=255, verbose_name='from account')),
                ('description', models.CharField(max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('amnt', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='\u0421\u0443\u043c\u043c\u0430')),
                ('pub_date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430')),
                ('status', models.CharField(choices=[('created', '\u0441\u043e\u0437\u0434\u0430\u043d'), ('processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), ('refund', '\u0441\u0434\u0435\u043b\u043a\u0430'), ('canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d')], default='created', max_length=40)),
                ('debit_credit', models.CharField(choices=[('in', 'debit'), ('out', 'credit')], default='in', max_length=40)),
            ],
            options={
                'verbose_name': 'Bank transfer',
                'verbose_name_plural': 'Bank transfers',
            },
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First name&Last name')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('nation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nation')),
                ('birthday', models.DateField(verbose_name='Birthday')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Long title')),
                ('short_title', models.CharField(blank=True, max_length=5, null=True, verbose_name='title')),
            ],
        ),
        migrations.CreateModel(
            name='InvestDeals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emission_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('finish_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('created', '\u0441\u043e\u0437\u0434\u0430\u043d'), ('processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), ('refund', '\u0441\u0434\u0435\u043b\u043a\u0430'), ('canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d')], default='created', max_length=40)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Lot of investments',
                'verbose_name_plural': 'Lots of investments',
            },
        ),
        migrations.CreateModel(
            name='InvestLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name of Lot')),
                ('amount', models.DecimalField(decimal_places=4, default='0.0', max_digits=10, verbose_name='Sum of lot to buy')),
                ('percent', models.DecimalField(decimal_places=4, default='0.0', max_digits=10, max_length=40, verbose_name='Percent objections on year')),
                ('working_days', models.IntegerField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.Currency', verbose_name='currency')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Lot of investments',
                'verbose_name_plural': 'Lots of investments',
            },
        ),
        migrations.CreateModel(
            name='Trans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance1', models.DecimalField(decimal_places=10, editable=False, max_digits=20, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f')),
                ('balance2', models.DecimalField(decimal_places=10, editable=False, max_digits=20, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f')),
                ('res_balance1', models.DecimalField(decimal_places=10, editable=False, max_digits=20, null=True, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f')),
                ('res_balance2', models.DecimalField(decimal_places=10, editable=False, max_digits=20, null=True, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f')),
                ('amnt', models.DecimalField(decimal_places=10, max_digits=20, verbose_name='\u0421\u0443\u043c\u043c\u0430')),
                ('status', models.CharField(choices=[('created', '\u0441\u043e\u0437\u0434\u0430\u043d'), ('processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), ('refund', '\u0441\u0434\u0435\u043b\u043a\u0430'), ('canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d')], default='created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.Currency', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_account', to='startpage.Accounts', verbose_name='\u0421\u0447\u0435\u0442 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_account', to='startpage.Accounts', verbose_name='\u0421\u0447\u0435\u0442 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Raw transaction',
                'verbose_name_plural': 'Raw transactions',
            },
        ),
        migrations.AddField(
            model_name='investdeals',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.InvestLot'),
        ),
        migrations.AddField(
            model_name='investdeals',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='banktransfers',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.Currency', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430'),
        ),
        migrations.AddField(
            model_name='banktransfers',
            name='user_accomplished',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operator_processed', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startpage.Currency', verbose_name='Currency'),
        ),
    ]
