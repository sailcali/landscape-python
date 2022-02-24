#!/usr/bin/env python3

import Adafruit_DHT as dht
import time
import RPi.GPIO as GPIO
import requests

DHT_TRIES = 6

def get_pi_details():
    """Access the onboard sensor and return temp and humidity"""
    global DHT_TRIES
    DHT_TRIES -= 1
    if DHT_TRIES == 0:
        return None, None
    sensor = dht.DHT22
    try:
        humidity, temperature = dht.read_retry(sensor, 4)
        farenheight = temperature * (9 / 5) + 32
        return farenheight, humidity
    except Exception:
        time.sleep(2)

def update_led(temp):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO_PIN = 17
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    response = requests.get('http://192.168.86.205/api/currrent_temps')
    current_temps = response.json()
    if current_temps['living_room_temp'] <= temp:
        if GPIO.input(GPIO_PIN):
            GPIO.output(GPIO_PIN, GPIO.LOW)
    else:
        if not GPIO.input(GPIO_PIN):
            GPIO.output(GPIO_PIN, GPIO.HIGH)

if __name__ == "__main__":
    temp, humidity = get_pi_details()
    update_led(temp)