from django.shortcuts import render
# from django.shortcuts import redirect
# from .models import Message
# from .forms import MessageForm


def search(request):
    return render(request, 'html/search.html')
