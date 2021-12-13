#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.OUT)

for i in range(14):
    city = lookup("San Diego", database())
    s = sun(city.observer, date=date.today())
    sunrise = s["sunrise"]
    sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
    sunset = s["sunset"]
    sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))

    print(sunrise.time())
    print(sunset.time())

    if sunset.time() < datetime.now().time() > sunrise.time():
        print('on')
        if GPIO.input(GPIO_PIN):
            print('is on')
        else:
            print('turning on')
            GPIO.output(GPIO_PIN, GPIO.HIGH)
    else:
        if not GPIO.input(GPIO_PIN):
            print('is off')
        else:
            print('turning off')
            GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(60)
GPIO.cleanup()
