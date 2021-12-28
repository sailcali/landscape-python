from flask import Flask, request, abort, jsonify, make_response
import RPi.GPIO as GPIO
from get_temps import get_pi_details
from main import change_landscape

app = Flask(__name__)

@app.route('/change-state', methods=['PUT'])
def change_landscape_state():
    body = request.get_json()
    GPIO_PIN = 27
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    change_landscape(body['state'], body['delay_time'])
    return make_response({'new_status': body['state'], 'new_delay': body['delay_time']}, 201)

@app.route('/get-status', methods=['GET'])
def get_status():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO_PIN = 27
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    temperature, humidity = get_pi_details()
    lighting_state = GPIO.input(GPIO_PIN)
    response = {'temperature': temperature, 'humidity': humidity, 
                'lighting_state': lighting_state}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
