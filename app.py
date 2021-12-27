from flask import Flask, request, abort, jsonify
import RPi.GPIO as GPIO
from get_temps import get_pi_details

app = Flask(__name__)


@app.route('/get-status', methods=['GET'])
def get_status():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO_PIN = 17
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    sensors = get_pi_details()
    return jsonify([GPIO.input(GPIO_PIN), sensors])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
