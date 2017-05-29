# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def index(response):
    'set a text to be displayed at index page'
    return HttpResponse("Hello, World! You're at the polls index.")
