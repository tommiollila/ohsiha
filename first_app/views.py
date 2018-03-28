from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmailForm, RegisterationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person, TrafficLightInformationTest, TrafficLightDetectors
import requests, json

def index(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['your_email']
            p = Person(email=email)
            p.save()
            return redirect('/your-email/')
    else:
        form = EmailForm()
    return render(request, "first_app/index.html", {'form': form})

def your_email(request):
    persons = Person.objects.all()
    return render(request, "first_app/your_email.html", {'persons': persons})

def jquery(request):
    return render(request, "first_app/jQuery.html")

def register(request):
    if request.method=="POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterationForm()
    args = {'form': form}
    return render(request, "first_app/register.html", args)

def base(request):
    if(request.POST.get('mybtn')):
        TrafficLightInformationTest.objects.all().delete()
    if(request.GET.get('dlAPI')):
        # Download the first JSON-file from API:
        r = requests.get('http://trafficlights.tampere.fi/api/v1/trafficAmount')
        text = r.text
        j_obj = json.loads(text)

        #Save all devices to database:
        device_length = len(j_obj["results"])
        i=0
        while i < device_length:
            device_name = j_obj["results"][i]["device"]
            detector_name = j_obj["results"][i]["detector"]
            device_object = TrafficLightDetectors(device=device_name)
            device_object.detector = detector_name
            device_object.save()
            i = i + 1

        #Give arguments to html-page of the devices:
        args = {'text': text}
        return render(request, "first_app/home.html", args)
    return render(request, "first_app/home.html")

def profile(request):
    args = {'user': request.user}
    return render(request, 'first_app/profile.html', args)

def edit_profile(request):
    if request.method=="POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = UserChangeForm(instance=request.user)
    args = {'form': form}
    return render(request, "first_app/editprofile.html", args)
