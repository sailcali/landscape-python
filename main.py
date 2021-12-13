#!/usr/bin/landscape-python/venv/bin/python3

import RPi.GPIO as GPIO
from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.OUT)

city = lookup("San Diego", database())
s = sun(city.observer, date=date.today())
sunrise = s["sunrise"]
sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
sunset = s["sunset"]
sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))

if sunset.time() < datetime.now().time():
    if GPIO.input(GPIO_PIN):
        pass
    else:
        GPIO.output(GPIO_PIN, GPIO.HIGH)
else:
    if not GPIO.input(GPIO_PIN):
        pass
    else:
        GPIO.output(GPIO_PIN, GPIO.LOW)
