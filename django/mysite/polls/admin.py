# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Choice, Poll


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')
    search_fields = ('choice_text', )
    list_filter = ('question', )

    class Meta:
        model = Choice


# Register your models here.
admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Poll)