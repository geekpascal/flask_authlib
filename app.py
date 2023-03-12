from flask import Flask, url_for, redirect, render_template, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'somecrazysecret'

# app.config['SERVER_NAME'] = 'localhost:5000'
app.config.from_object('config')

oauth = OAuth(app)

GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    # client_id=GOOGLE_CLIENT_ID,
    # client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/google/')
def google():
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
 
@app.route('/google/auth/')  
def google_auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']    
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

 
if __name__ == "__main__":
    app.run(debug=True)

