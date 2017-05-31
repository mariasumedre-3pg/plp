from django.core.management.base import BaseCommand

#from polls.models import Poll, Question
#import faker

class Command(BaseCommand):
    help = 'Generates some mock poll data'

    def handle(self, *args, **kwargs):
        print 'run command funkydata'
        pass