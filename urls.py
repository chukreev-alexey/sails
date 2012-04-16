# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from autocomplete.views import autocomplete

admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url('^autocomplete/', include(autocomplete.urls)),
    #url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name="logout"),
    url(r'^password/reset/$', 'password_reset', name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete',
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', 'password_reset_done',
        name='auth_password_reset_done'),
)

urlpatterns += patterns('website.views',
    url(r'^$', 'order_list', name='order_list'),
    url(r'^orders/$', 'order_list', name='order_list'),
    url(r'^new/order/$', 'new_order', name='new_order'),
    url(r'^order/(?P<pk>\d+)/$', 'order_info', name='order_info'),
    url(r'^confirm/payments/(?P<pk>\d+)/$', 'confirm_payment', name='confirm_payment'),
    url(r'^report/payments/$', 'report_payments', name='report_payments'),

    url(r'^cashorder/(?P<pk>\d+)/$', 'cash_order', name='cash_order'),

    # Ajax requests
    url(r'^change/payment/comment/$', 'change_payment_comment', name='change_payment_comment'),

    url(r'^login/$', 'login', name="login"),
    url(r'^messages/$', 'message_list', name='message_list'),
    url(r'^messages/(.*)/$', 'message_list', name='message_list'),
)

# Serving static
if settings.DEBUG:
    urlpatterns += patterns('django.views',
        url(r'^media/(?P<path>.*)$', 'static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
