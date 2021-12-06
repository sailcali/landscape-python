#!/usr/bin/env python3

# import gpiozero
import time

from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup

city = lookup("San Diego", database())
s = sun(city.observer, date=date.today())
sunrise = s["sunrise"]
sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
sunset = s["sunset"]
sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))

print(sunrise.time())
print(sunset.time())

relay = gpiozero.OutputDevice(17, active_high=True, initial_value=False)
# if relay.value:
relay.off()
print(relay.value)
time.sleep(15)
