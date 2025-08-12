import os
import markdown
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from iac_assistant import process_iac_request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# A secret key is required for using sessions in Flask
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page.
    GET: Displays the input form.
    POST: Processes the user's request, stores the result in the session,
          and redirects to the result page.
    """
    if request.method == 'POST':
        user_request = request.form.get('prompt', '').strip()
        if not user_request:
            return render_template('index.html', error="Request cannot be empty.")

        # Process the request using the core logic from iac_assistant.py
        result = process_iac_request(user_request)

        # Store the result and original request in the session
        session['result_data'] = result
        session['user_request'] = user_request
        
        # Redirect to the results page (Post/Redirect/Get pattern)
        return redirect(url_for('results'))

    return render_template('index.html')


@app.route('/results')
def results():
    """Displays the results of the IaC generation and scan."""
    result_data = session.get('result_data')
    user_request = session.get('user_request')

    if not result_data or not user_request:
        return redirect(url_for('index'))

    # Convert markdown report to HTML for rendering
    if 'report' in result_data:
        result_data['report_html'] = markdown.markdown(result_data['report'], extensions=['fenced_code', 'tables'])

    return render_template('result.html', result=result_data, user_request=user_request)


if __name__ == '__main__':
    app.run(debug=True)
