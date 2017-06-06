# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Choice, Poll


class InlineChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 2


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')
    search_fields = ('choice_text', )
    list_filter = ('question', )

    class Meta:
        model = Choice


class QuestionAdmin(admin.ModelAdmin):
    ' specify how the admin page for a question looks like '
    inlines = [InlineChoiceAdmin, ]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date",)
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    search_fields = ("question_text","choice__choice_text")
    list_per_page = 50

    class Meta:
        ' model for admin is Question '
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