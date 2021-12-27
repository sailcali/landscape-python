import Adafruit_DHT as dht
import time

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
        sensor.exit()
        return farenheight, humidity
    except Exception:
        time.sleep(2)
        sensor.exit()