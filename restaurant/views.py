from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

#create view here

def home(request):
    '''Fun to respond to the "home" request.'''

    template_name = 'restaurant/main.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)


def main(request):
   '''main.html'''
   template_name = 'restaurant/main.html'
   return render(request, template_name)

def order(request):
    '''Respond to the URL 'order', delegate work to a template.'''

    template_name = 'restaurant/order.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    } 
    return render(request, template_name, context)

def confirmation(request):
    '''Respond to the URL 'confirmation', delegate work to a template.'''

    template_name = 'restaurant/confirmation.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    }
    
    return render(request, template_name, context)
