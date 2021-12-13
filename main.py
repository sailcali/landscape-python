#!/usr/bin/landscape-python/venv/bin/python3

import RPi.GPIO as GPIO
from astral.sun import sun
from datetime import date
import pytz
from astral.geocoder import database, lookup
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv, set_key, find_dotenv
import os
import pandas as pd

# Set globals
DOTENV_FILE = find_dotenv()
load_dotenv(DOTENV_FILE)
DB_STRING = os.environ.get('DB_STRING')
data = {'time': [datetime.today(),], 'device': 'landscape'}

# Open database engine
db = create_engine(DB_STRING)

# Get last time entry from database
with db.connect() as con:
    sql = """SELECT time FROM lighting_status WHERE device = 'landscape' ORDER BY time DESC LIMIT 1;"""
    result = con.execute(sql)
    last_time = result.fetchone()[0]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.OUT)

city = lookup("San Diego", database())
s = sun(city.observer, date=date.today())
sunrise = s["sunrise"]
sunrise = sunrise.astimezone(tz=pytz.timezone("US/Pacific"))
#sunset = s["sunset"] - timedelta(hours=8) # FOR TESTING ONLY
sunset = s["sunset"]
sunset = sunset.astimezone(tz=pytz.timezone("US/Pacific"))

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
        time_on = datetime.now() - last_time
        data['time_on'] = time_on.seconds
        
# Create dataframe from sensor data
df = pd.DataFrame(data)
df.set_index(['time'], inplace=True)

# Send new data to database
df.to_sql('lighting_status', db, if_exists='append')
