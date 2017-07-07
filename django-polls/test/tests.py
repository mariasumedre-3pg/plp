# -*- coding: utf-8 -*-
'unit test for polls app: views and models and all'
from __future__ import unicode_literals
import datetime

from django.test import TestCase
from django.test import Client
from django.utils import timezone
from django.urls import reverse

import pytest

from polls.models import Question, Poll

# Create your tests here.
class QuestionMethodTests(TestCase):
    """ class to test the question model """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for
        questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False if
        the question is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True if
        the question is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    """ test for the questions view -> actually poll view now """
    urls = 'mysite.polls.urls'
    fixtures = []

    def setUp(self):
        """ make a new Client """
        # Every test needs a client.
        self.client = Client()
        for poll in Poll.objects.all():
            poll.delete()

    def test_index_with_no_questions(self):
        """
        If no questiones exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_polls'], [])

    def test_index_with_a_past_question(self):
        """
        If there is a question in the far past, then that question shall be displayed.
        """
        question = create_question("Test an old question?", -3)
        poll = Poll.objects.create(name="Test past question")
        poll.questions.add(question)
        poll.clean()
        poll.save()
        response = self.client.get(reverse('polls:detail', args=(poll.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test an old question?")
        self.assertEqual(response.context['poll'], poll)

    def test_index_with_a_future_question(self):
        """
        If there is a question in the near past, less than a day,
        then that question shall be displayed
        """
        create_question("Test a recent question?", 3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_polls'], [])

    def test_index_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed
        """
        question = create_question(question_text="Past question.", days=-30)
        question2 = create_question(question_text="Future question.", days=30)
        poll = Poll.objects.create(name="Test past question")
        poll.questions.add(question)
        poll.questions.add(question2)
        poll.clean()
        poll.save()
        response = self.client.get(reverse('polls:detail', args=(poll.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question.")
        self.assertNotContains(response, "Future question.")
        self.assertEqual(response.context['poll'], poll)

    def test_index_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-5)
        question2 = create_question(question_text="Past question 2.", days=-7)
        poll = Poll.objects.create(name="Test past question")
        poll.questions.add(question1)
        poll.questions.add(question2)
        poll.clean()
        poll.save()
        response = self.client.get(reverse('polls:detail', args=(poll.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question 1.")
        self.assertContains(response, "Past question 2.")
        self.assertEqual(response.context['poll'], poll)


class QuestionIndexDetailTests(TestCase):
    urls = 'mysite.polls.urls'

    def setUp(self):
        """ make a new Client """
        # Every test needs a client.
        self.client = Client()
        for poll in Poll.objects.all():
            poll.delete()

    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 200 but without the future question
        """
        future_question = create_question(question_text='Future question.', days=4)
        poll = Poll.objects.create(name="Test future question")
        poll.questions.add(future_question)
        poll.clean()
        poll.save()
        url = reverse('polls:detail', args=(poll.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Future question.")

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display a question's test.
        """
        past_question = create_question(question_text='Past Question.', days=-2)
        poll = Poll.objects.create(name="Test past question")
        poll.questions.add(past_question)
        poll.clean()
        poll.save()
        url = reverse('polls:detail', args=(poll.slug,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


@pytest.mark.django_db
def test_it():
    pass