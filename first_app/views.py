from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import EmailForm, RegisterationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person, TrafficLightDetectors, DegreeCoordinates
import requests, json, re

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
        j=0
        file = open("coordinates.txt", "w")
        while i < length:
            json_intersection = j_obj["features"][i]["properties"]["LIITTYMAN_NRO"]
            type = j_obj["features"][i]["properties"]["TUNNUS"]
            if type == None or json_intersection == None:
                pass
            else:
                new_type = str.lower(type.replace('-', '_'))
                try:
                    asked_object = TrafficLightDetectors.objects.get(detector=new_type, intersection=json_intersection)
                    x_dot = j_obj["features"][i]["geometry"]["coordinates"][0]
                    y_dot = j_obj["features"][i]["geometry"]["coordinates"][1]
                    asked_object.n_coordinate = y_dot
                    asked_object.e_coordinate = x_dot

                    str_x = str(x_dot)
                    str_y = str(y_dot)

                    file.write(str_y + " " + str_x + '\n')

                    file2 = open("coordinates2.txt", "r+")
                    lines = [line.rstrip('\n') for line in file2]
                    corrected_line = ("".join(lines[j].split()))
                    first_index = corrected_line.find("'", 8)
                    second_index = first_index - 5

                    x_coordinat = corrected_line[second_index:]
                    y_coordinat = corrected_line[:second_index]

                    x_coordinate = x_coordinat + "'E"
                    y_coordinate = y_coordinat + "'N"

                    asked_object.y_coo = y_coordinate
                    asked_object.x_coo = x_coordinate

                    asked_object.longitude = parse_dms(x_coordinate)
                    asked_object.latitude = parse_dms(y_coordinate)

                    asked_object.save()

                    j = j + 1

                except TrafficLightDetectors.DoesNotExist:
                    pass
            i = i + 1
        file.close()

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

def get_coordinates(request):
    objects = TrafficLightDetectors.objects.all().exclude(latitude=None)
    json_object={}
    for object in objects:
        json_object[object.id] = {'lon': object.longitude,
                    'lat': object.latitude,
                    }
    return JsonResponse(json_object, safe=False)

#LOCAL FUNCTIONS:

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'E' or direction == 'N':
        dd *= -1
    return dd;

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(parts[0], parts[1], parts[2], parts[3])
    return (lat)
