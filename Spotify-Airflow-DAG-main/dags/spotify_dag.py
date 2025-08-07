from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
import base64

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

load_dotenv()
TOKEN = os.getenv('TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

GET_PLAYLIST_URL = 'https://api.spotify.com/v1/me/playlists'
AUTHORIZATION_URL = 'https://accounts.spotify.com/api/token'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 6),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_trial': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

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
        "Authorization" : f'Bearer {token}'
    }
    r = requests.get(GET_PLAYLIST_URL, headers = headers)
    print(r)


spotify_dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Spotify DAG',
    schedule_interval=timedelta(days=1)
)

playlist_task = PythonOperator(
    task_id='get_playlist_task',
    python_callable=get_playlist,
    provide_context=True,
    dag=spotify_dag
)

auth_task = PythonOperator(
    task_id='get_auth_token',
    python_callable=authorize_user,
    provide_context=True,
    dag=spotify_dag
)

auth_task >> playlist_task