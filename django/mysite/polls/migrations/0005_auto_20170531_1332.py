# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 13:32
""" this is a migration that adds data to database,
    using some random generators from Faker """

from __future__ import unicode_literals
from django.utils import timezone
from django.utils import text
from django.db import migrations
import faker


def clean(obj):
    ''' copied clean method from Poll, as model methods don't work here '''
    today = timezone.now()
    # add in the slug - future url also the date of the poll
    # but without the minutes, meaning that if you make 2 polls with similar names
    # then there will be an error
    obj.slug = text.slugify(obj.name + today.strftime('-%d-%B-%Y'))

def slugify(name):
    ''' copied clean method from Poll, as model methods don't work here '''
    today = timezone.now()
    return text.slugify(name + today.strftime('-%d-%B-%Y'))

def help_create_a_question(question_class, question_text, func):
    ''' utility to create a question with
        provided text using a func from Faker
        called 5 times (5 choices) '''
    question = question_class.objects.create(question_text=question_text,
                                             pub_date=timezone.now())
    for _ in range(5):
        question.choice_set.create(choice_text=func())
    return question

def help_create_a_poll(question_class, poll_class, dictionary, poll_name):
    ''' utility to create a poll with
        provided questions and Faker functions
        in the dictionary '''
    print "creating poll %s" % poll_name
    poll = poll_class.objects.create(name=poll_name, slug=slugify(poll_name))
    #clean(poll) # add the slug
    # questions are created with a simple helper function, in a list comprehension
    # which is then unpacked
    poll.questions.add(*[
        help_create_a_question(question_class, question_text, dictionary[question_text])
        for question_text in dictionary.keys()
    ])
    poll.save() # i found this necessary so the slug is also updated in the db
    return poll

def add_workforce_poll(poll_class, question_class, generator):
    """ function to add the workforce poll to database using help_create_a_poll
        it was done to make the insert_data function lighter """
    workforce_poll_dictionary = {
        'What is your name?': generator.name,
        'What is your address?': generator.address,
        'What is your job?': generator.job,
        'Where do you work?': generator.company
    }
    workforce_poll = help_create_a_poll(
        question_class, poll_class, workforce_poll_dictionary, 'Workforce Poll'
    )
    print "%s was introduced in database ..." % workforce_poll.slug

def add_random_poll(poll_class, question_class, generator):
    """ function to add the random questions poll to database using help_create_a_poll
        it was done to make the insert_data function lighter """
    random_poll_dictionary = {
        'When is your birthday?': generator.date,
        'What is your phone number?': generator.phone_number,
        'Where are you from?': generator.country,
        'What is your best quality?': generator.catch_phrase
    }
    random_poll = help_create_a_poll(
        question_class, poll_class, random_poll_dictionary, "Random Poll"
    )
    print "%s was introduced in database ..." % random_poll.slug

def insert_data(apps, schema_editor):
    ''' insert 2 polls in the database,
        polls are created using faker generators '''
    print "starting migration to insert 2 polls in database ..."
    # the models are taken from history in case they were changed <- take old version
    # as opposed to taking them through from polls.models import Poll, Question
    # Choice is not needed, it will be used in Question directly
    poll_class = apps.get_model("polls", "Poll")
    question_class = apps.get_model("polls", "Question")
    generator = faker.Faker()

    add_workforce_poll(poll_class, question_class, generator)
    add_random_poll(poll_class, question_class, generator)


def delete_data(apps, schema_editor):
    'test2'
    poll_class = apps.get_model("polls", "Poll")
    question_class = apps.get_model("polls", "Question")

    polls_questions = [
        'What is your name?', 'What is your address?', 'What is your job?', 'Where do you work?',
        'When is your birthday?', 'What is your phone number?', 'Where are you from?',
        'What is your best quality?'
    ]
    for question_text in polls_questions:
        question_class.objects.filter(question_text=question_text).delete()
    print "deleting added questions ..."

    poll_class.objects.filter(name='Workforce Poll').delete()
    print "Workforce Poll was deleted from database ..."
    poll_class.objects.filter(name='Random Poll').delete()
    print "Random Poll was deleted from database ..."


class Migration(migrations.Migration):
    """ migration to add some data (polls + questions + choices) to database """
    dependencies = [
        ('polls', '0004_auto_20170530_1634'),
    ]

    operations = [
        migrations.RunPython(insert_data, delete_data)
    ]
