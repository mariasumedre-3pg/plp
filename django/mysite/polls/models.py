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
        today = timezone.now()
        self.slug = self.slug or text.slugify(self.name + today.strftime('-%d-%B-%Y'))

    @models.permalink
    def get_absolute_url(self):
        ' something url '
        #equivalent to
        # from django.urls import reverse
        # return reverse('polls:poll', args=[str(self.slug)])
        return 'polls:poll', (self.slug,)

    def __unicode__(self):
        return self.name
