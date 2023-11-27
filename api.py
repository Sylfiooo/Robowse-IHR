import requests
import json, urllib2

api_key = "38843eff9addea0e39391ee2c8e87927"
lat = "45.764043"
lon = "4.835659"


url="http://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid=38843eff9addea0e39391ee2c8e87927"
weatherbot=urllib2.urlopen(url)
weatherinfo = json.load(weatherbot)
current_temp=weatherinfo["main"]["temp"]-273.15

