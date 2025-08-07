import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()
TOKEN = os.getenv('TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

GET_PLAYLIST_URL = 'https://api.spotify.com/v1/me/playlists'
AUTHORIZATION_URL = 'https://accounts.spotify.com/api/token'

def authorize_user(**kwargs):
    credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f'Basic {encoded_credentials}'
    }
    payload = {
        "grant_type": "client_credentials"
    }
    res = requests.post(AUTHORIZATION_URL, headers=headers, data=payload)
    status_code = res.status_code
    res = res.json()
    if status_code == 200:
        token = res.get('access_code')
        kwargs['ti'].xcom_push(key='spotify_token', value=token)

def get_playlist(**kwargs):
    token = kwargs['ti'].xcom_pull(key='spotify_token')
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : 'Bearer {token}'
    }
    r = requests.get(GET_PLAYLIST_URL, headers = headers)
    print(r)

