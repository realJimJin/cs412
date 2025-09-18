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
   # a dict of context variables (key-value pairs)
   context = {
        "time": time.ctime(),
    }
   return render(request, template_name, context)

def order(request):
    '''Respond to the URL 'order', delegate work to a template.'''

    template_name = 'restaurant/order.html'
    # a dict of context variables (key-value pairs)
    context = {
        "time": time.ctime(),
    } 
    return render(request, template_name, context)


def confirmation(request):
    '''Process the form submission, and generate a result.'''

    template_name = "restaurant/confirmation.html"
    print(request.POST)

    # check if POST data was sent with the HTTP POST message:
    if request.POST:

        # extract form fields into variables:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']  

        # create context variables for use in the template
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'time': time.ctime(), 
            'special_instructions': special_instructions,
        } 

        # delegate the response to the template, provide context variables
        return render(request, template_name=template_name, context=context)
