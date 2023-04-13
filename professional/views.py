# from django.shortcuts import render
from django.http import HttpResponse


def home():
    return HttpResponse('<h1>Professional Home Page</h1>')


def register():
    return HttpResponse('<h1>Register as a professional page</h1>')
