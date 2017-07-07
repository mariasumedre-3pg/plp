""" command makefunkydata will load a json passed as param and will add the info in the db
    format:
        Poll
            pollName - str
            questions - list of Question
        Question
            questionName - str
            choices - list of str
        """
import json

from django.core.management.base import BaseCommand
from django.utils import timezone, text

from polls.models import Poll, Question, Choice


def read_file(filepath):
    ''' read file and return the strings within in a list of strings '''
    lines = []
    with open(filepath, 'r') as fpointer:
        lines = json.load(fpointer)
    return lines

def slugify(name):
    ' use django.utils.text.slugify on poll name and current hour+min+sec'
    today = timezone.now()
    return text.slugify(name + today.strftime("-%H-%M-%S"))

class Command(BaseCommand):
    'Generates some mock poll data'
    help = 'Generates some mock poll data'

    def add_arguments(self, parser):
        'add arguments'
        parser.add_argument('json', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        'run command makefunkydata'
        print 'run command makefunkydata'
        data_path = kwargs['json'] if 'json' in kwargs else ''
        if data_path and data_path[0]:
            data = read_file(data_path[0])
            for pdata in data:
                pname = pdata['pollName']
                poll = Poll.objects.create(name=pname, slug=slugify(pname))
                print '... adding poll:', poll.name,
                for qdata in pdata['questions']:
                    question = Question.objects.create(question_text=qdata['questionName'],
                                                       pub_date=timezone.now())
                    for cdata in qdata['choices']:
                        choice = Choice.objects.create(choice_text=cdata, question=question)
                        choice.save()
                        question.choice_set.add(choice)
                    question.save()
                    poll.questions.add(question)
                poll.clean()
                poll.save()
                print "... done"

