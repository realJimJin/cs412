from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

#create view here

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
