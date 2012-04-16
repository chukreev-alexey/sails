# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pytils.numeral import rubles

from common.fields import MultiEmailField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^common\.fields\.MultiEmailField"])


class VisibleObjects(models.Manager):
    def get_query_set(self):
        return super(VisibleObjects, self).get_query_set().filter(visible=True)

class Settings(models.Model):
    project = models.CharField(u'Название проекта', max_length=255)
    email = MultiEmailField(u'Email для писем', max_length=255,
        help_text=u'''Можете вставить несколько email, разделив их запятой''')
    firm = models.CharField(u'Название фирмы', max_length=255, default='')
    n_pay = models.IntegerField(u'Следующий номер приходника', default=0)
    head_booker = models.CharField(u'Главный бухгалтер в приходник',
        max_length=255, default='')
    
    def __unicode__(self):
        return u'настройки'
    
    def delete(self):
        return False
        
    class Meta:
        verbose_name = u'настройки'
        verbose_name_plural = u'настройки'

@receiver(post_save, sender=Settings)
@receiver(post_delete, sender=Settings)
def clear_settings_cache(sender, **kwargs):
    cache.delete('settings')

class Country(models.Model):
    name = models.CharField(u'Название', max_length=255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'страна'
        verbose_name_plural = u'страны'

class Oper(models.Model):
    name = models.CharField(u'Название', max_length=255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'туроператор'
        verbose_name_plural = u'туроператоры'

class Currency(models.Model):
    name = models.CharField(u'Название', max_length=255)
    code = models.CharField(u'HTML код', max_length=10)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'валюта'
        verbose_name_plural = u'валюты'
        
class Office(models.Model):
    name = models.CharField(u'Название (адрес) офиса', max_length=255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'офис'
        verbose_name_plural = u'офисы'
    
class Staff(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Логин')
    office = models.ForeignKey(Office, verbose_name=u'офис')
    name = models.CharField(u'ФИО сотрудника', max_length=255)
    
    def get_group_list(self):
        return ",".join([item.name for item in self.user.groups.all()])
    get_group_list.short_description = u'Группы'
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'сотрудник'
        verbose_name_plural = u'сотрудники'

class Order(models.Model):
    staff = models.ForeignKey(Staff, verbose_name=u'менеджер заявки')
    dt_mod = models.DateTimeField(u'Дата создания', default=datetime.datetime.now)
    tourist = models.CharField(u'Турист', max_length=255)
    country = models.ForeignKey(Country, verbose_name=u'страна')
    dt_in = models.DateField(u'Дата заезда')
    oper = models.ForeignKey(Oper, verbose_name=u'оператор')
    order_value = models.DecimalField(u'Сумма по договору', max_digits=15, decimal_places=4)
    currency = models.ForeignKey(Currency, verbose_name=u'валюта')
    comment = models.TextField(u'Комментарий', blank=True, null=True)
    
    def __unicode__(self):
        return u"№%d от %s %s %s %s" % (
            (self.pk or 0), self.dt_mod.strftime('%d.%m.%y %H:%M'), self.tourist,
            self.country, self.dt_in.strftime('%d.%m.%y'))
    
    def get_payments_sum(self):
        return sum([pay[0] / (pay[1] or 1) \
                    for pay in self.payments.values_list('pay', 'rate')])
    
    def get_debt(self):
        return self.order_value - self.get_payments_sum()
    
    class Meta:
        ordering = ('-dt_mod', )
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки'



class PaymentType(models.Model):
    name = models.CharField(u'Название', max_length=255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name', )
        verbose_name = u'форма платежа'
        verbose_name_plural = u'формы платежей'


class Payment(models.Model):
    n_pay = models.IntegerField(u'Номер приходника', default=0)
    payment_type = models.ForeignKey(PaymentType, blank=True, null=True,
        verbose_name=u'форма платежа', related_name='payments')
    dt_mod = models.DateTimeField(u'Дата создания', default=datetime.datetime.now)
    order = models.ForeignKey(Order, verbose_name=u'заявка', related_name='payments')
    staff = models.ForeignKey(Staff, verbose_name=u'менеджер платежа',
        related_name='managers',)
    pay = models.DecimalField(u'Сумма платежа в рублях', max_digits=15, decimal_places=4)
    rate = models.DecimalField(u'Курс платежа', max_digits=15, decimal_places=4)
    checked_by = models.ForeignKey(Staff, verbose_name=u'Проверено пользователем',
        related_name='checkers', blank=True, null=True)
    comment = models.TextField(u'Комментарий', blank=True, null=True)
    
    def __unicode__(self):
        return u"%.2f р. з.%d" % (self.pay, self.order.id)
    
    def get_rubles(self):
        return rubles(self.pay, True)
        
    def save(self, *args, **kwargs):
        try:
            setts = Settings.objects.all()[0]
            n_pay = setts.n_pay
            setts.n_pay = n_pay + 1
            setts.save()
        except IndexError:
            n_pay = 0
        self.n_pay = n_pay
        super(Payment, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-dt_mod', )
        verbose_name = u'платеж'
        verbose_name_plural = u'платежи'
    
    
    
    
    
    
    
    
    
    
    
    