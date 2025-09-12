from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

#create view here

quotes = ["Be yourself; everyone else is already taken", "Life is too important to be taken seriously", "I can resist everything except temptation"]
images = ["data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==","https://the-public-domain-review.imgix.net/essays/on-oscar-wilde-and-plagiarism/23565530654_c3ae721476_o.jpg?fit=max&w=1200&h=850&auto=format,compress", "https://publicdomainlibrary.org/uploads/attachments/livhezziviv05628j5rfyihf-oscar-wilde-by-napoleon-sarony-three-quarter-length-photograph-seated.max.webp" ]

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
        "image_url": images[random.randint(0,2)],
        "quote": quotes[random.randint(0,2)], 
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
