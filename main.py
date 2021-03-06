#!/usr/bin/env python3

import os
os.chdir('/var/www/landscape-API')

import RPi.GPIO as GPIO
from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime, timedelta
import requests
import configparser
import logging

def change_landscape(on_off=3, delay_request=False):
    logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    config = configparser.ConfigParser()
    config.read_file(open(r'delay_time.conf'))
    if delay_request:
        config.set('DelayDatetime', 'value', datetime.strftime(delay_request, '%Y-%m-%d %H:%M:%S'))
        with open('delay_time.conf', 'w') as configfile:
            config.write(configfile)
    value = config.get('DelayDatetime', 'value')
    delay_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    logging.info('config opened')
    data = {'time': datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'), 'device': 'landscape'}

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO_PIN = 27
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    logging.info('GPIO set')
    city = lookup("San Diego", database())
    s = sun(city.observer, date=date.today())
    sunrise = s["sunrise"]
    sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
    sunset = s["sunset"] + timedelta(minutes=15)
    
    sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))
    
    if on_off == 1 and not GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        data['state'] = True
        logging.info(requests.post('http://192.168.86.205/landscape/update-state', json=data))
        return
    
    elif on_off == 0 and GPIO.input(GPIO_PIN):
        GPIO.output(GPIO_PIN, GPIO.LOW)
        data['state'] = False
        logging.info(requests.post('http://192.168.86.205/landscape/update-state', json=data))
        return
    logging.info('on_off tree complete')
    
    if delay_datetime > datetime.today():
        return

    logging.info('delay_datetime OK')
    logging.info(GPIO.input(GPIO_PIN))
    if sunset.time() < datetime.now().time():
        if GPIO.input(GPIO_PIN):
            return
        else:
            GPIO.output(GPIO_PIN, GPIO.HIGH)
            data['state'] = True
    else:
        if not GPIO.input(GPIO_PIN):
            return
        else:
            GPIO.output(GPIO_PIN, GPIO.LOW)
            data['state'] = False
            
    # Send new data to database
    requests.post('http://192.168.86.205/landscape/update-state', json=data)
    logging.info('update sent')
if __name__ == '__main__':
    change_landscape()
