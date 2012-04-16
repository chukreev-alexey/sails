# -*- coding: utf-8 -*-
import datetime

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.utils import simplejson
from django.db.models import Q, Sum

from common.fields import emails_list
from common.utils import get_paginator

from website.models import Order, Payment
from website.utils import is_auth_manager, is_auth_direction

@login_required
def order_list(request):
    from website.forms import OrderListFilterForm
    form = OrderListFilterForm(request.GET or None)
    if is_auth_manager(request.user):
        del(form.fields['office'])
        del(form.fields['staff'])
    query = Q()

    if request.GET.get('order', False):
        query = query & Q(pk=request.GET['order'])
    else:
        if request.GET.get('tourist', False):
            query = query & Q(tourist__icontains=request.GET['tourist'])
        if request.GET.get('country', False):
            query = query & Q(country__id=request.GET['country'])
        if request.GET.get('office', False):
            query = query & Q(staff__office__id=request.GET['office'])
        if request.GET.get('staff', False):
            query = query & Q(staff__id=request.GET['staff'])
        if request.GET.get('dt1', False):
            dt = datetime.datetime.strptime(request.GET['dt1'], '%d.%m.%Y').date()
            query = query & Q(dt_in__gte=dt)
        else:
            query = query & Q(dt_in__gte=datetime.date.today())
        if request.GET.get('dt2', False):
            dt = datetime.datetime.strptime(request.GET['dt2'], '%d.%m.%Y').date()
            query = query & Q(dt_in__lte=dt)

        if is_auth_manager(request.user): # Фильтрация по менеджеру
            if request.GET.get('forders', False):
                query = query & Q(staff__office=request.account.office)
            else:
                query = query & Q(staff=request.account)

    queryset = Order.objects.filter(query)
    object_list = get_paginator(request, queryset, rows_on_page=30)
    return render(request, 'order_list.html',
        {'object_list': object_list, 'form': form})

@transaction.commit_on_success
@login_required
def new_order(request):
    from website.forms import NewOrderForm
    form = NewOrderForm(request.POST or None)

    if form.is_valid():
        staff = request.user.get_profile()
        order = Order(
            staff=staff,
            tourist=form.cleaned_data['tourist'],
            country=form.cleaned_data['country'],
            dt_in=form.cleaned_data['dt_in'],
            oper=form.cleaned_data['oper'],
            order_value=form.cleaned_data['order_value'],
            currency=form.cleaned_data['currency'],
            comment=form.cleaned_data['order_comment'])
        order.save()
        pay = Payment(
            payment_type=form.cleaned_data['pay_type'],
            order=order, staff=staff,
            pay=form.cleaned_data['pay'], rate=form.cleaned_data['rate'],
            comment=form.cleaned_data['pay_comment'])
        pay.save()
        messages.add_message(request, messages.SUCCESS,
            u"Заявка успешно зарегистрирована под номером - %d." % order.id)
        return redirect('message_list')
    return render(request, 'new_order.html', {'form': form})

@login_required
@user_passes_test(is_auth_direction)
def report_payments(request):
    from website.forms import PaymentReportForm
    form = PaymentReportForm(request.POST or None)
    query = Q()
    if form.is_valid():
        if request.POST.get('dt1', False):
            dt = datetime.datetime.strptime(request.POST['dt1'], '%d.%m.%Y').date()
            query = query & Q(dt_mod__gte=dt)
        if request.POST.get('dt2', False):
            dt = datetime.datetime.strptime(request.POST['dt2'], '%d.%m.%Y').date() + \
                 datetime.timedelta(days=1)
            query = query & Q(dt_mod__lte=dt)
        if request.POST.get('office', False):
            query = query & Q(staff__office=request.POST['office'])
        if request.POST.get('staff', False):
            query = query & Q(staff=request.POST['staff'])
        if request.POST.get('status', False):
            if request.POST['status'] == 'yes':
                query = query & Q(checked_by__isnull=False)
            if request.POST['status'] == 'no':
                query = query & Q(checked_by__isnull=True)
    if query:
        object_list = Payment.objects.select_related('order').filter(query)
        object_list.total_row = object_list.aggregate(pay=Sum('pay'))
    else:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        object_list = Payment.objects.select_related('order').filter(
            dt_mod__range=[today, tomorrow])
        object_list.total_row = object_list.aggregate(pay=Sum('pay'))
    return render(request, 'reports/payment_list.html',
        {'object_list': object_list, 'form': form})

@transaction.commit_on_success
@login_required
def order_info(request, pk):
    from website.forms import NewPaymentForm
    object_detail = get_object_or_404(Order, pk=pk)
    form = NewPaymentForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            pay = Payment(payment_type=form.cleaned_data['pay_type'],
                order=object_detail, staff=request.account,
                pay=form.cleaned_data['pay'], rate=form.cleaned_data['rate'],
                comment=form.cleaned_data['pay_comment'])
            pay.save()
            messages.add_message(request, messages.SUCCESS,
                u"Оплата уcпешно добавлена")
            return HttpResponse('')
        else:
            return HttpResponse(simplejson.dumps({'errors': form.errors}),
                                mimetype='text/javascript')
    return render(request, 'boxes/order_info_box.html',
        {'object_detail': object_detail, 'form': form})

@transaction.commit_on_success
@login_required
def confirm_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if payment.checked_by:
        raise Http404
    payment.checked_by = request.account
    payment.save()
    return render(request, 'boxes/payment_status_box.html', {'item': payment})

@login_required
def cash_order(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'docs/cash_order.html', {'payment': payment})
    
@login_required
@user_passes_test(is_auth_direction)
def change_payment_comment(request):
    from .forms import PaymentCommentForm
    form = PaymentCommentForm(request.POST)
    if form.is_valid():
        payment = get_object_or_404(Payment, pk=form.cleaned_data['payment'])
        comment = form.cleaned_data["comment"]
        if comment:
            comment = u"%s (%s)" % (form.cleaned_data["comment"], request.account.name)
        payment.comment = comment
        payment.save()
        return HttpResponse('ok')
    else:
        raise Http404
    
@csrf_protect
@never_cache
def login(request):
    from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
    from website.forms import LoginForm
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL

            if not form.cleaned_data['remember']:
                request.session.set_expiry(0)

            auth_login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)
    else:
        form = LoginForm(request)
    request.session.set_test_cookie()
    return render(request, 'login.html',
        {'form': form, REDIRECT_FIELD_NAME: redirect_to})

def message_list(request, arg=None):
    return render(request, 'messages.html')

def feedback(request):
    from website.forms import FeedbackForm
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = u'Вопрос с сайта'
            recipients = []
            recipients.extend(emails_list(request.settings.email))
            letter_context = form.cleaned_data
            letter_context.update({'site': request.settings.project})
            letter_content = render_to_string('feedback_letter.txt', letter_context)
            send_mail(subject, letter_content,
                      letter_context['email'] or recipients[0], recipients)
            messages.add_message(request, messages.SUCCESS, u"Ваше письмо успешно отправлено администрации сайта.")
            return redirect('')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})