from django.http import HttpResponse
from django.shortcuts import render
from .forms import EmailForm

def index(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
    else:
        form = EmailForm()
    return render(request, "first_app/index.html", {'form': form})

def your_email(request):
    return render(request, "first_app/your_email.html")
