# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class SessionManagementMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse('index'):
            return redirect('homepage1')
        if not request.user.is_authenticated and request.path.startswith(reverse('homepage1')):
            messages.add_message(request, messages.ERROR, 'Your session has expired. Please log in again.')
            return redirect('login')
        
        response = self.get_response(request)
        return response
