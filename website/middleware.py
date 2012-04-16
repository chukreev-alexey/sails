# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import redirect
from django.core.cache import cache
from django.conf import settings
from django.contrib import messages

from website.models import Settings, Staff
from website.utils import is_auth_manager, is_auth_direction

class BeforeViewMiddleware(object):
    
    def __init__(self):
        pass
    
    def common_actions(self, request):
        request.settings = cache.get('settings')
        if not request.settings:
            try:
                request.settings = Settings.objects.all()[0]
                cache.set('settings', request.settings, 60*60*24)
            except:
                pass
        
        return request
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.PROJECT_TITLE = settings.PROJECT_TITLE
        
        if not view_func.__module__ in ('website.views', ):
            return None
        
        request = self.common_actions(request)
        if request.user.is_authenticated():
            try:
                request.account = request.user.get_profile()
            except Staff.DoesNotExist:
                if request.path != settings.LOGIN_URL:
                    messages.error(request, u'К учетной записи %s не привязан ни один сотрудник. Обратитесь к администратору.' % request.user)
                    return redirect(settings.LOGIN_URL)
            request.is_auth_manager = is_auth_manager(request.user)
            request.is_auth_direction = is_auth_direction(request.user)
        
        return None
