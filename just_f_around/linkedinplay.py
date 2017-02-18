from flask import Flask, request, redirect, url_for, render_template
import requests
import json


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!'

TOKEN = 'AQUjSTlVFjhzd0TG8xR1-hQbiY7Tb29ZdTqHXBARMwKFQcoXJB9QPpvN11_fiamADGtgSoGtRuVj6YfKGh-1wb7i6tvVWKzf3oSXEmk_ftAKR-uQFriwmFFoDo5AiqGZYNi2n8wjf1aQsH9jVIsMTVFuJ2uKdlJoAMIaESUEz3QZ2lIBtTU'
client_id = '77eo269xhh3u7q'
client_secret = 'ywsnbntpB92vHsec'
redirect_uri = 'http://localhost:5000/auth'

auth_url = 'https://www.linkedin.com/oauth/v2/authorization'
auth_params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'state': 'ohoGOIOGO6755-'
}

token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
token_params = {
    'grant_type': 'authorization_code',
    'code': '',
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}


@app.route('/linkedin')
def linkedin_authorize():
    return redirect(requests.get(auth_url, params=auth_params).url)


@app.route('/auth')
def request_token():
    code = request.args.get('code', '')
    state = request.args.get('state', '')

    try:
        assert state == auth_params['state']
    except:
        return 'Error 401'

    token_params['code'] = code

    r = requests.post(token_url, data=token_params)
    global TOKEN
    TOKEN = json.loads(r.text)['access_token']
    return redirect(url_for('authorization_success'))


@app.route('/success')
def authorization_success():
    headers = {
        'authorization': TOKEN,
        'connection': 'keep-alive'
    }

    params = {
        'oauth2_access_token': TOKEN
    }

    fields = (
        'id',
        'first-name',
        'last-name',
        'headline',
        'location',
        'industry',
        'num-connections',
        'positions',
        'picture-url',
        'site-standard-profile-request',
        'api-standard-profile-request',
        'public-profile-url',
        'email-address'
    )

    r = requests.get(
        'https://api.linkedin.com/v1/people/~:(' + ','.join(fields) + ')?format=json', params=params)

    data = json.loads(r.text)
    return render_template('success.html',
                           fields=fields,
                           data=data,
                           )

#'Authorization success. Token: ' + TOKEN
