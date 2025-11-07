# app.py
from flask import Flask, send_file, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import pytz
from datetime import datetime
import os

app = Flask(__name__)

# Prometheus counters
gandalf_counter = Counter('gandalf_requests_total', 'Total requests to /gandalf')
colombo_counter = Counter('colombo_requests_total', 'Total requests to /colombo')

@app.route('/gandalf')
def gandalf():
    gandalf_counter.inc()
    # Make sure you have gandalf.jpg in a static folder
    return send_file('static/gandalf.jpg', mimetype='image/jpeg')

@app.route('/colombo')
def colombo():
    colombo_counter.inc()
    colombo_tz = pytz.timezone('Asia/Colombo')
    current_time = datetime.now(colombo_tz)
    return jsonify({
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': 'Asia/Colombo'
    })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=8080)





