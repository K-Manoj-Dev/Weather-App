from django.shortcuts import render,redirect
#this is a forms.py class Name CityForm
from .forms import CityForm
#here i import City because of i need City Objects
from .models import City
#import Request
import requests
from django.contrib import messages


def home(request):
    #here i paste weather app url 
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},&appid=d9d900c3ca8783b544ba47259eff8646&units=metric'
    
    #after that i go to insert city codesy
    if request.method == "POST":
        form = CityForm(request.POST)
        print(form)
        if form.is_valid():
            NCity = form.cleaned_data['name']
            CCity = City.objects.filter(name=NCity).count()
            if CCity == 0:
                res = requests.get(url.format(NCity)).json()
                #print(res)
                if res['cod'] == 200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully...!!!") #this messages code is written in weatherapp.html 
                else:
                    messages.error(request, "City Does Not Exists...!!!")
            else:
                messages.error(request, "City Already Exists...!!!")

    #here i am going to create object of CityForm
    form = CityForm()
    cities = City.objects.all() #this is City Object all the city nameonce stored in database. i need to show all of them that's why i write this code into weatherapp.html check it.
    
    data = []
    #after collected all objects then we ned to show cities name in json format 
    for city in cities:
        res = requests.get(url.format(city)).json() #it requests from url to json show into like all the object weather report json format.
        # print(res)

        #here i want collect weather cityname icon date time country 
        city_weather = {
            'city':city,
            'temprature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'country': res['sys']['country'],
            'icon': res['weather'][0]['icon'],
            }
        #this all collect from res variable main inside has a temp  so that i mentioned like this res['main']['temp'] i can collect temprature, same way to collect all the bellow data.
        #after collected all reports. i go to append report into varibale data like list wise.
        data.append(city_weather)
    context = {'data':data, 'form':form}
    return render(request, "weatherapp.html", context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect("Home")

