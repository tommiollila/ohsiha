from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import EmailForm
from .models import Person

def index(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['your_email']
            p = Person(email=email)
            p.save()
            return HttpResponseRedirect('/your-email/')
    else:
        form = EmailForm()
    return render(request, "first_app/index.html", {'form': form})

def your_email(request):
    persons = Person.objects.all()
    return render(request, "first_app/your_email.html", {'persons': persons})

def jquery(request):
    return render(request, "first_app/jQuery.html")

def base(request):
    return render(request, "base.html")
