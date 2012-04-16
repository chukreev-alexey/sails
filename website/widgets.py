# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms

class CalendarWidget(forms.DateInput):
    format = '%d.%m.%Y'
    class Media:
        js = (
            settings.MEDIA_URL + 'jquery/js/jquery-ui.min.js',
            settings.MEDIA_URL + 'jquery/js/jquery.datepicker.js', 
            settings.MEDIA_URL + 'jquery/js/jquery.ui.datepicker-ru.js', 
        )
    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(attrs={
            'class': 'vCalendarField', 'size': '10'})
