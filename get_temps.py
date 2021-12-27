import adafruit_dht as dht
from board import D4
import time

DHT_TRIES = 6

def get_pi_details():
    """Access the onboard sensor and return temp and humidity"""
    global DHT_TRIES
    DHT_TRIES -= 1
    if DHT_TRIES == 0:
        return None, None
    sensor = dht.DHT22(D4)
    try:
        farenheight = sensor.temperature * (9 / 5) + 32
        hum = sensor.humidity
        sensor.exit()
        return farenheight, hum
    except Exception:
        time.sleep(2)
        sensor.exit()