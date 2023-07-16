import urllib.request
import json
import urllib.error
import ssl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='MyApp')
city = input('Enter city: ')

location = geolocator.geocode(city)
try:
    print("Latitude", location.latitude, "\nLongitude", location.longitude)
except AttributeError:
    print('Cannot find this city')
    quit()
url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&" \
      f"longitude={location.longitude}&hourly=temperature_2m,precipitation&timezone=Europe%2FBerlin"
print(url)


def update(val):
    d = day.val
    x = time[(d - 1) * 24:d * 24]
    y = temperature[(d - 1) * 24:d * 24]
    z = precipitation[(d - 1) * 24:d * 24]
    l.set_data(x, y)
    b.set_data(x, z)
    ax.grid(True)
    ax.set_yticks(np.arange(min(y), max(y), 0.5))
    ax.set_ylim([min(y) - 0.5, max(y) + 0.5])
    ax.set_xlim([min(x), max(x)])

    if all(numbers == 0.0 for numbers in z):
        ax2.set_yticks(np.arange(0, 0.1, 0.1))
        ax2.set_ylim([0 - 0.1, 0.1 + 0.1])
    else:
        ax2.set_yticks(np.arange(min(z), max(z), (max(z) - min(z)) / 12))
        ax2.set_ylim([min(z) - 0.1, max(z) + 0.1])

    plt.savefig(f'weather{day.val}.jpg')

def load_data(address_url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url_open = urllib.request.urlopen(address_url, context=ctx)
    data = url_open.read().decode()

    return json.loads(data)


js = load_data(url)
time_data = js['hourly']['time']
temperature = js['hourly']['temperature_2m']
precipitation = js['hourly']['precipitation']
time = list()
for i in range(len(time_data)):
    time.append(time_data[i][-5:-3])

fig, ax = plt.subplots()
ax2 = ax.twinx()
title = 'Krakow temperature and precipitation ' + (time_data[0][0:10]) + '  --  ' + (time_data[-1][0:10])
plt.title(title)
ax.set_xlabel('Time [hour]')
ax.set_ylabel('Temperature [Celsius]')
ax2.set_ylabel('Precipitation [mm]')

l, = ax.plot(time[0:24], temperature[0: 24], label='temperature', color='red')
b, = ax2.plot(time[0:24], precipitation[0:24], label='precipitation', color='blue')

day_axes = plt.axes([0.2, 0.97, 0.65, 0.03])
day = Slider(day_axes, 'Day', valmin=1, valmax=7, valstep=1)

update(day)
day.on_changed(update)

ax.legend(handles=[l, b])
wm = plt.get_current_fig_manager()
wm.window.state('zoomed')
plt.show()

