#!/usr/bin/env python3

import RPi.GPIO as GPIO
from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime
import requests
import configparser
import logging

def change_landscape(on_off=False, delay_request=False):
    logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    config = configparser.ConfigParser()
    config.read_file(open(r'delay_time.conf'))
    value = config.get('DelayDatetime', 'value')
    delay_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M')
    if delay_request:
        config.set('DelayDatetime', 'value', delay_request)
        with open('delay_time.conf', 'w') as configfile:
            config.write(configfile)
    logging.info('config opened')
    data = {'time': datetime.today(), 'device': 'landscape'}

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO_PIN = 27
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    logging.info('GPIO set')
    city = lookup("San Diego", database())
    s = sun(city.observer, date=date.today())
    sunrise = s["sunrise"]
    sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
    #sunset = s["sunset"] - timedelta(hours=8) # FOR TESTING ONLY
    sunset = s["sunset"]
    sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))
    
    if on_off == 1 and not GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        data['state'] = True
        requests.post('http://192.168.86.31/landscape/update-state', params=data)
        return
    
    elif on_off == 0 and GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.LOW)
        data['setting'] = False
        requests.post('http://192.168.86.31/landscape/update-state', params=data)
        return
    logging.info('on_off tree complete')
    if delay_datetime > datetime.today():
        return
    logging.info('delay_datetime OK')
    if sunset.time() < datetime.now().time():
        if GPIO.input(GPIO_PIN):
            quit()
        else:
            GPIO.output(GPIO_PIN, GPIO.HIGH)
            data['setting'] = True
    else:
        if not GPIO.input(GPIO_PIN):
            quit()
        else:
            GPIO.output(GPIO_PIN, GPIO.LOW)
            data['setting'] = False
            
    # Send new data to database
    requests.post('http://192.168.86.31/landscape/update-state', params=data)
    logging.info('update sent')
if __name__ == '__main__':
    change_landscape()
