from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

#create view here

quotes = ["Be yourself; everyone else is already taken", "Life is too important to be taken seriously", "I can resist everything except temptation"]
images = ["https://www.flickriver.com/photos/trialsanderrors/3318337409/","https://publicdomainreview.org/essay/on-oscar-wilde-and-plagiarism", "https://publicdomainlibrary.org/en/authors/oscar-wilde" ]

def home(request):
    '''Fund to respond to the "home" request.'''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>
    </html> 
    '''

    return HttpResponse(response_text) 


def base(request):
   '''base.html'''
   template_name = 'quotes/base.html'
   return render(request, template_name) 

def about(request):
    '''Respond to the URL 'about', delegate work to a template.'''

    template_name = 'quotes/about.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)

def quote(request):
    '''Respond to the URL 'about', delegate work to a template.'''

    template_name = 'quotes/quote.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL 'about', delegate work to a template.'''

    template_name = 'quotes/show_all.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)
