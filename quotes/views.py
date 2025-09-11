from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

#create view here

def home(request):
'''Fund to respond to the "home" request.'''

response_text = '''
<html>
<h1>Hello, world!</h1>
</html> 
'''

return HttpResponse(response_text) 




