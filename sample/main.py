from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response,send_from_directory
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
 
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
 
# Initialize Flask app
app = Flask(__name__, template_folder='D:/Final_logincode/sample (1)/sample/templates')
app.secret_key = '12345'# Secret key for session management'
 
# Cloudant DB credentials (replace with actual values)
CLOUDANT_URL = "64a60d3e-c958-42ea-9252-6f66c57f3e3f-bluemix.cloudantnosqldb.appdomain.cloud"  # Cloudant service URL
API_KEY = "AIyxGRsO1w4ce9tzJK2rvUnEyAUOUaM5sd-gJEx_PWfH"  # Cloudant API Key
DB_NAME = "cloudantai"  # Cloudant database name
 
# Initialize Cloudant client
authenticator = IAMAuthenticator(API_KEY)
client = CloudantV1(authenticator=authenticator)
client.set_service_url(f'https://{CLOUDANT_URL}')
 
# Verify connection to Cloudant
try:
    client.get_server_information().get_result()
except ApiException as e:
    print(f"Error connecting to Cloudant: {e}")
    exit(1)
 
# Route to home/login page
@app.route('/')
def home():
#    template_path = os.path.join(app.root_path, 'templates', 'login.html')
#    print(f"looking for template at: {template_path}")
    return render_template('login.html')
 
# Route to handle login form submission
 
@app.route('/login', methods=['POST'])
def login():
    username_form = request.form['username']
    password_form = request.form['password']
 
    # Query Cloudant DB to check if user exists
    try:
        response = client.post_find(
            db=DB_NAME,
            selector={"username": username_form},
            fields=["username", "password", "access_analytics_dashboard"],
            limit=1
        ).get_result()
 
        if response['docs']:
            user = response['docs'][0]
            if user['password'] == password_form:
                # Check if user has access to login
                if user.get('access_analytics_dashboard', True):
                    # Store user session
                    session['username'] = user['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    #flash('Please contact administrator for access!', 'danger')
                    return redirect(url_for('dashboard_error'))
            else:
                flash('Invalid password!', 'danger')
        else:
            flash('User not found!', 'danger')
 
    except ApiException as e:
        flash(f"Error querying Cloudant DB: {e}", 'danger')
 
    return redirect(url_for('home'))
 
 
# Route for the dashboard page (after successful login)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to login first!', 'danger')
        return redirect(url_for('home'))
#    return redirect(url_for('https://watsonxce3.1pska4xfp7g7.us-south.codeengine.appdomain.cloud/servicedesk'))
 
    return render_template('dashboard.html')
 
@app.route('/dashboard_error')
def dashboard_error():
    return render_template('dashboard_error.html')
    #image_path = os.path.join(app.root_path,'static','error_image.png')
    #return send_from_directory(os.path.dirname(image_path),'error_image.png')
 
 
# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
 
# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)