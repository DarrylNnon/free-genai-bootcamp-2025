from flask import Flask, render_template, request, jsonify
import awsgi
from main import orchestrate_iac_generation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_request = data.get('prompt')
    if not user_request:
        return jsonify({'error': 'No prompt provided'}), 400

    final_report = orchestrate_iac_generation(user_request)
    return jsonify({'report': final_report})

def lambda_handler(event, context):
    # Use awsgi to wrap the Flask app for Lambda compatibility
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
