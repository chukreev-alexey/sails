# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm

#from supercaptcha import CaptchaField
from autocomplete.utils import autocomplete_formfield
from autocomplete.widgets import AutocompleteWidget

from website.models import (Currency, Order, Payment, Country, Oper, Staff,
                            Office, PaymentType)
from website.widgets import CalendarWidget

def as_eul(self):
    return self._html_output(
        normal_row = u'<li%(html_class_attr)s><div class="FormLabel">%(label)s</div> <div class="FormField">%(field)s</div><div class="FormError">%(errors)s</div><div class="FormHelpText">%(help_text)s</div></li>',
        error_row = u'<li>%s</li>',
        row_ender = '</li>',
        help_text_html = u' %s',
        errors_on_separate_row = False)
forms.BaseForm.as_eul = as_eul

class LoginForm(AuthenticationForm):
    remember = forms.BooleanField(label=u'Запомнить меня', required=False)


class OrderListFilterForm(forms.Form):
    order = forms.CharField(label=u'Номер заявки', required=False)
    tourist = forms.CharField(label=u'ФИО', required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
        label=u'Страна', widget=AutocompleteWidget(Order.country),
        required=False)
    office = forms.ModelChoiceField(queryset=Office.objects.all(),
        label=u'Офис', required=False)

    staff = forms.ModelChoiceField(queryset=Staff.objects.all(),
        label=u'Менеджер', widget=AutocompleteWidget(Order.staff),
        required=False)

    dt1 = forms.DateField(label=u'Дата заезда c', widget=CalendarWidget,
        initial=datetime.date.today, required=False)
    dt2 = forms.DateField(label=u'Дата заезда по', widget=CalendarWidget,
        required=False)
    forders = forms.BooleanField(label=u'Искать в заявках менеджеров офиса',
        required=False)

class PaymentReportForm(forms.Form):
    CHECKED_CHOICES = (
        ('all', u'Все'),
        ('yes', u'Проверено'),
        ('no', u'Не проверено'),
    )
    dt1 = forms.DateField(label=u'Дата платежа c', widget=CalendarWidget,
        initial=datetime.date.today,)
    dt2 = forms.DateField(label=u'Дата платежа по', widget=CalendarWidget,
        initial=datetime.date.today,)
    office = forms.ModelChoiceField(queryset=Office.objects.all(),
        required=False, label=u'Офис')
    staff = forms.ModelChoiceField(queryset=Staff.objects.all(), required=False,
        label=u'Менеджер', widget=AutocompleteWidget(Payment.staff))
    status = forms.ChoiceField(label=u'Статус платежей',
        choices=CHECKED_CHOICES)

class NewOrderForm(forms.Form):
    tourist = forms.CharField(label=u'ФИО')
    oper = forms.ModelChoiceField(queryset=Oper.objects.all(),
        label=u'Оператор', widget=AutocompleteWidget(Order.oper))
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
        label=u'Страна', widget=AutocompleteWidget(Order.country))
    dt_in = forms.DateField(label=u'Дата заезда', widget=CalendarWidget)
    order_value = forms.DecimalField(label=u'Сумма по договору')
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(),
        label=u'Валюта', empty_label=u' -- ', required=True)
    order_comment = forms.CharField(label=u'Комментарий к заявке',
        widget=forms.Textarea, required=False)
    pay = forms.DecimalField(label=u'Сумма платежа')
    pay_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(),
        label=u'Форма платежа', empty_label=u' -- ')
    rate = forms.DecimalField(label=u'Курс платежа')
    pay_comment = forms.CharField(label=u'Комментарий к оплате',
        widget=forms.Textarea, required=False)

class NewPaymentForm(forms.Form):
    pay = forms.DecimalField(label=u'Сумма платежа')
    pay_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(),
        label=u'Форма платежа', empty_label=u' -- ')
    rate = forms.DecimalField(label=u'Курс платежа')
    pay_comment = forms.CharField(label=u'Комментарий к оплате',
        widget=forms.Textarea, required=False)

class PaymentCommentForm(forms.Form):
    payment = forms.IntegerField(label=u'ИД платежа')
    comment = forms.CharField(label=u'Комментарий к оплате', required=False)
