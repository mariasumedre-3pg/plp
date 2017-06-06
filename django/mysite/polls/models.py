# -*- coding: utf-8 -*-
""" has all the db models of the polls application -> question and choice so far """
from __future__ import unicode_literals

import datetime

from django.utils import text
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    """ db model of a question, it has a date, a text and choices """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        ' return whether the question was published less than a day ago '
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """ db model for a choice, it belongs to a question and has votes """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
        )
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Poll(models.Model):
    ''' poll holds questions (but might share the questions with other polls)
# Poll Question  PollQuestion
# 1     2           1 2
# 3     3           1 3
    '''
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) # save the name sluggified
    questions = models.ManyToManyField(Question, blank=True)

    def clean(self):
        # add in the slug - future url also the date of the poll
        # but without the minutes, meaning that if you make 2 polls with similar names
        # then there will be an error
        today = timezone.now()
        self.slug = self.slug or text.slugify(self.name + today.strftime('-%d-%B-%Y'))

    def get_questions(self):
        ' helper method to not display future questions '
        return self.questions.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

    def __unicode__(self):
        return self.name
