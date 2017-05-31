# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Choice, Poll


class InlineChoiceAdmin(admin.TabularInline):
    model = Choice


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')
    search_fields = ('choice_text', )
    list_filter = ('question', )

    class Meta:
        model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [InlineChoiceAdmin, ]

    class Meta:
        model = Question


class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')

    def count(self, obj):
        return obj.questions.all().count()

    class Meta:
        model = Poll



# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Poll, PollAdmin)