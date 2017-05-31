# -*- coding: utf-8 -*-
""" has the methods instructing how to create the views for the polls app:
    index, detail, results, obsolete-vote """
from __future__ import unicode_literals
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
#from django.template import loader

from django.http import HttpResponseRedirect#, HttpResponse, Http404
from django.urls import reverse
from django.views import generic

from django.db.models import F
from .models import Question, Choice, Poll


# Create your views here.
class IndexView(generic.ListView):
    """ class sub-classing listview to help us displaya list of questions """
    template_name = 'polls/index.html'
    context_object_name = 'latest_polls'

    def get_queryset(self):
        return Poll.objects.all()

    # def get_queryset(self):
    #     'returns last (at most) 5 questions asked'
    #     return Question.objects.filter(
    #         pub_date__lte=timezone.now()
    #         ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """ class sub-classing detailview helping us display a question """
    model = Poll
    template_name = 'polls/detail.html'
    # the name of the argument for slug is 'slug'
    slug_url_kwarg = 'slug'
    # we are sending a slug, not necessarily a pk
    query_pk_and_slug = True


class ResultsView(generic.DetailView):
    """ class sub-classing detailview helping us display votes of a question """
    model = Poll
    template_name = 'polls/results.html'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True


#keep the old version of the function to remember what was replaced with the class
def results(request, question_id):
    """ function that does the same thing as class resultsview
        displays votes of a question """
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    context = {
        'question': question,
        'choices': choices,
    }
    return render(request, 'polls/results.html', context)

def vote(request, pk):
    """ function to display the vote page - obsolete """
    poll = get_object_or_404(Poll, pk=pk)
    #choices = []
    result = None
    try:
        choices = [question.choice_set.get(pk=request.POST[question.question_text])
                   for question in poll.questions.all()]
        #for question in poll.questions.all:
        #    selected_choice = question.choice_set.get(pk=request.POST[question.question_text])
        #    choices.append[selected_choice]
    except (KeyError, Choice.DoesNotExist):
        result = render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        for selected_choice in choices:
            selected_choice.votes = F('votes') + 1
            selected_choice.save()
        result = HttpResponseRedirect(reverse('polls:results', args=(poll.slug,)))

    return result
