from django.shortcuts import render
# from django.shortcuts import redirect
# from .models import Message
# from .forms import MessageForm


def indexView(request):
    return render(request, 'html/index.html')