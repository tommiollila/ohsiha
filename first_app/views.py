from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmailForm, RegisterationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person, TrafficLightDetectors
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
        TrafficLightDetectors.objects.all().delete()

    if(request.GET.get('locationsBtn')):
        objects = TrafficLightDetectors.objects.all()
        r = requests.get('http://opendata.navici.com/tampere/opendata/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=opendata:WFS_LIIKENNEVALO_ILMAISIN&outputFormat=json')
        text = r.text
        j_obj = json.loads(text)

        length = len(j_obj["features"])
        i=0
        while i < length:
            json_intersection = j_obj["features"][i]["properties"]["LIITTYMAN_NRO"]
            type = j_obj["features"][i]["properties"]["TUNNUS"]
            if type == None or json_intersection == None:
                pass
            else:
                new_type = str.lower(type.replace('-', '_'))
                try:
                    asked_object = TrafficLightDetectors.objects.get(detector=new_type, intersection=json_intersection)
                    print("Taalla")
                    x_dot = j_obj["features"][i]["geometry"]["coordinates"][0]
                    y_dot = j_obj["features"][i]["geometry"]["coordinates"][1]
                    #print(x_dot + " " + y_dot)
                    asked_object.longitude = x_dot
                    asked_object.latitude = y_dot
                    asked_object.save()
                except TrafficLightDetectors.DoesNotExist:
                    pass
            i = i + 1

        args = {'objects': objects}
        return render(request, "first_app/home.html", args)

    if(request.GET.get('amountBtn')):
        objects = TrafficLightDetectors.objects.all()
        args = {'objects': objects}
        r = requests.get('http://trafficlights.tampere.fi/api/v1/trafficAmount/')
        text = r.text
        j_obj = json.loads(text)

        if len(j_obj["results"]) == 0:
            return render(request, "first_app/home.html", args)
        amount_device_length = len(j_obj["results"])
        i=0
        while i < amount_device_length:
            if TrafficLightDetectors.objects.filter(detector=j_obj["results"][i]["detector"], device=j_obj["results"][i]["device"]).exists():
                asked_object = TrafficLightDetectors.objects.get(detector=j_obj["results"][i]["detector"], device=j_obj["results"][i]["device"])
                trafficAmount = j_obj["results"][i]["trafficAmount"]
                asked_object.traffic_amount = trafficAmount
                asked_object.save()
                i = i + 1

        return render(request, "first_app/home.html", args)

    if(request.GET.get('dlAPI')):
        r = requests.get('http://trafficlights.tampere.fi/api/v1/trafficAmount')
        text = r.text
        j_obj = json.loads(text)

        device_length = len(j_obj["results"])
        i=0
        while i < device_length:
            if TrafficLightDetectors.objects.filter(detector=j_obj["results"][i]["detector"], device=j_obj["results"][i]["device"]).exists():
                pass
            else:
                device_name = j_obj["results"][i]["device"]
                detector_name = j_obj["results"][i]["detector"]
                device_object = TrafficLightDetectors(device=device_name)
                intersection_name = device_name[3:]
                device_object.detector = detector_name
                device_object.device = device_name
                device_object.intersection = intersection_name
                device_object.save()
            i = i + 1

        objects = TrafficLightDetectors.objects.all()
        args = {'objects': objects}
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

def map(request):
    return render(request, "first_app/map.html")
