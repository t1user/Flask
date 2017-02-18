from flask import Flask, request, redirect, url_for
import requests
import json


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!'

TOKEN = '36340039.08d86d3.fc4b5b5c67c74738968bb9d86f6a04cd'

instagram_params = {
    'client_id': '08d86d355e56481a8d77127e59c7b0c4',
    'client_secret': '76af6863ee3d4b3da7c490ec512bc565',
    'redirect_uri': 'http://localhost:5000/auth',
    'response_type': 'code',
    'scope': 'public_content',
    'grant_type': 'authorization_code',
    'code': ''
}


def get_params(*args):
    param_string = ''
    for i in args:
        param_string += str(i) + '=' + instagram_params[i] + '&'
    param_string = param_string[:-1]
    return param_string


def get_params_dict(*args):
    param_dict = {}
    for i in args:
        param_dict[i] = instagram_params[i]
    return param_dict


@app.route('/login')
def get_code():
    url_base = "https://api.instagram.com/oauth/authorize/?"
    url = url_base + get_params('client_id', 'redirect_uri',
                                'response_type', 'scope')
    print(url)
    return redirect(url)


@app.route('/auth')
def response_handler():
    try:
        code = request.args.get('code', '')
        print('got code:', code)
        instagram_params['code'] = code
        url = 'https://api.instagram.com/oauth/access_token'
        d = get_params_dict('client_id', 'client_secret',
                            'grant_type', 'redirect_uri',
                            'code')

        print(d)
        r = requests.post(url, data=d)
        print(r.url)
        return r.text
        # return redirect(url_for('present_token', token=r))
    except:
        return "Error"
    """
        try:
            token = request.args.get('access_token', '')
            print (token)
            print (request.args)
            return "Your access token: " + str(token)
        except:
            return "I don't know what the fuck is going on"
    """


@app.route('/present_token/<token>')
def present_token(token):
    return token

"""
@app.route('/get_token/<code>')
def get_token(code):
    print('in the redirect function')

    

   
    params = get_params('client_id', 'client_secret',
                        'grant_type', 'redirect_uri',
                        'code')
   
    # url = base_url + params
    # print(url)

    return r
"""


def results_string(arg):
    res_str = ''
    for i in arg:
        res_str += str(i) + '/n'
    return res_str


@app.route('/location')
def get_location_pics():
    params = {
        'lat': '51.486409',
        'lng': '-0.178981',
        'distance': '5000',
        'access_token': TOKEN
    }

    url = 'https://api.instagram.com/v1/media/search'

    r = requests.get(url, params)
    print(r.url)
    #results = json.loads(r.text)

    return r.text


@app.route('/id')
def loc_id():
    location_id = '624750006'
    url_base = 'https://api.instagram.com/v1/locations/'
    ext = location_id + '/media/recent?access_token=' + TOKEN

    url = url_base + ext

    r = requests.get(url)
    return r.text


@app.route('/search')
def search():
    params = {
        'facebook_places_id': 'Warsaw',
        'access_token': TOKEN
    }

    url = 'https://api.instagram.com/v1/locations/search'

    r = requests.get(url, params)

    return r.text
