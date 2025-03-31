from flask import Flask, jsonify, request
import logging
import uuid
from pythonjsonlogger import jsonlogger
import requests

app = Flask(__name__)

log = logging.getLogger("service1_logger")
logHandler = logging.FileHandler('/app/logs/service1.log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s request_id=%(request_id)s, source=%(source)s, destination=%(destination)s')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)
log.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request.request_id = request_id
    log.info("Received request for Service 1 with Request ID: %s", request_id)

@app.route('/forward')
def forward():
    request_id = request.request_id
    headers = {
        'X-Request-ID': request_id,
        'From-Service1': 'true'
    }

    if 'From-Service2' not in request.headers:
        log.info("Forwarding request to Service 2", extra={'request_id': request_id, 'source': request.url, 'destination': 'http://service2:5002/'})
        
        response = requests.get('http://service2:5002/', headers=headers)
        response_body = response.text

        log.info("Response from Service 2: %s", response_body)
        return response_body
    else:
        log.info("Already handled by Service 2", extra={'request_id': request_id, 'source': request.url})
    return "Hello from Service 2!"

@app.route('/')
def home():
    return "Hello from Service 1!"

AUTH_SERVICE_URL = 'http://auth_service:5000/validate'

@app.route('/data', methods=['GET'])
def get_service_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': "Token is missing!"}), 403
    response = requests.post(AUTH_SERVICE_URL, headers={'Authorization': token})
    if response.status_code != 200:
        return jsonify({"message": "Access denied!"}), 403
    return jsonify({"message": "Access granted to Service 1 data!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
