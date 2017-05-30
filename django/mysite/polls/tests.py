# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
class QuestionMethodTests(TestCase):

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
    def test_index_with_no_questions(self):
        """
        If no questiones exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_index_with_a_past_question(self):
        """
        If there is a question in the far past, then that question shall be displayed.
        """
        question = create_question("Test an old question?", -3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test an old question?")
        self.assertQuerysetEqual(response.context['latest_questions'], [repr(question)])

    def test_index_with_a_future_question(self):
        """
        If there is a question in the near past, less than a day,
        then that question shall be displayed
        """
        create_question("Test a recent question?", 3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_index_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question.")
        self.assertNotContains(response, "Future question.")
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            [repr(question)]
        )

    def test_index_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-5)
        question2 = create_question(question_text="Past question 2.", days=-7)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            [repr(question1), repr(question2)]
        )
