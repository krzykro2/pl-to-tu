from flask import Flask, jsonify, request

from transform import polish_to_turkish_ortography

app = Flask(__name__)

@app.route('/')
def serve_index():
  return app.send_static_file('index.html')

@app.route('/transform', methods=['POST'])
def transform_request():
  return jsonify({'payload': polish_to_turkish_ortography(request.json['payload'])})
