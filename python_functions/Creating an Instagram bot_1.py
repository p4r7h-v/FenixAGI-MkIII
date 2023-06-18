import requests
from requests.structures import CaseInsensitiveDict
from urllib.parse import urlencode
import json

def main():
    app_id = 'YOUR_APP_ID'
    app_secret = 'YOUR_APP_SECRET'
    redirect_uri = 'YOUR_REDIRECT_URI'

    auth_url = get_auth_url(app_id, redirect_uri)
    print('Visit the following URL to authorize the app:')
    print(auth_url)

    code = input('Copy the authorization code and enter it here: ')
    access_token = get_access_token(code, app_id, app_secret, redirect_uri)

    user_info = get_user_info(access_token)
    print('User Information:')
    print(json.dumps(user_info, indent=2))

def get_auth_url(app_id, redirect_uri):
    base_url = 'https://api.instagram.com/oauth/authorize'
    params = {
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': 'user_profile',
        'response_type': 'code'
    }
    return f'{base_url}?{urlencode(params)}'

def get_access_token(code, app_id, app_secret, redirect_uri):
    url = 'https://api.instagram.com/oauth/access_token'
    data = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    
    headers = CaseInsensitiveDict()
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f'Failed to get access token: {response.text}')

def get_user_info(access_token):
    url = f'https://graph.instagram.com/me?fields=id,username&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to get user info: {response.text}')

if __name__ == '__main__':
    main()