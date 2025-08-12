import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import markdown2

from iac_assistant import process_iac_request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    """Renders the main page."""
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint to handle IaC generation requests."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_request = data.get("request")

    if not user_request:
        return jsonify({"error": "No request provided"}), 400

    # Call the main processing logic from our assistant
    result = process_iac_request(user_request)

    # Convert the markdown report to HTML for easy rendering
    if "report" in result and result["report"]:
        result["report_html"] = markdown2.markdown(result["report"], extras=["fenced-code-blocks", "tables"])

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
