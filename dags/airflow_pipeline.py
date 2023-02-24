import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy import exc
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import datetime, timedelta


def get_auth_token():
    auth_url = 'https://id.twitch.tv/oauth2/token'
    cred = {
        'client_id': Variable.get('CLIENT_ID'),
        'client_secret': Variable.get('CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    }

    r = requests.post(auth_url, data=cred)
    data = r.json()
    access_token = data['access_token']
    return access_token


def get_api_data(**context):
    base_url = 'https://api.igdb.com/v4'
    header = {'Client-ID': Variable.get('CLIENT_ID'),
              'Authorization': 'Bearer ' + context['task_instance'].xcom_pull(task_ids='get_auth_token')}

    r = requests.post(base_url + '/games', headers=header,
                      data='''fields name, category, first_release_date, status,
    aggregated_rating, aggregated_rating_count, rating, rating_count,
    total_rating, total_rating_count; where category = 0; limit 100;''')
    games_table = r.json()
    games_table_df = pd.DataFrame(games_table)

    r = requests.post(base_url + '/games', headers=header,
                      data='fields genres; limit 100;')
    genres_table = r.json()
    genres_table_df = pd.DataFrame(genres_table).explode('genres')

    r = requests.post(base_url + '/games', headers=header,
                      data='fields keywords; limit 100;')
    keywords_table = r.json()
    keywords_table_df = pd.DataFrame(keywords_table).explode('keywords')

    r = requests.post(base_url + '/games', headers=header,
                      data='fields platforms; limit 100;')
    platforms_table = r.json()
    platforms_table_df = pd.DataFrame(platforms_table).explode('platforms')

    r = requests.post(base_url + '/genres', headers=header, data='fields name; limit 500;')
    genre_info_table = r.json()
    genre_info_table_df = pd.DataFrame(genre_info_table)

    r = requests.post(base_url + '/keywords', headers=header, data='fields slug; limit 100;')
    keyword_info_table = r.json()
    keyword_info_table_df = pd.DataFrame(keyword_info_table)

    r = requests.post(base_url + '/platforms', headers=header, data='fields name; limit 100;')
    platform_info_table = r.json()
    platform_info_table_df = pd.DataFrame(platform_info_table)

    return {'games': games_table_df, 'genres': genres_table_df, 'keywords': keywords_table_df,
            'platforms': platforms_table_df, 'genre_info': genre_info_table_df, 'keyword_info': keyword_info_table_df,
            'platform_info': platform_info_table_df}


def clean_data(**context):
    # Grab previous task values
    dfs = context['task_instance'].xcom_pull(task_ids='get_api_data')
    games_table_df = dfs['games']
    genres_table_df = dfs['genres']
    genre_info_table_df = dfs['genre_info']
    keywords_table_df = dfs['keywords']
    keyword_info_table_df = dfs['keyword_info']
    platforms_table_df = dfs['platforms']
    platform_info_table_df = dfs['platform_info']

    # Renaming df tables to sync with DB Schema
    # Games Table:
    games_clean = games_table_df.rename(columns={"id": "game_id"})

    # Genre Tables:
    genres_clean = genres_table_df.rename(columns={"id": "game_id", "genres": "genre_id"})
    genre_info_clean = genre_info_table_df.rename(columns={"id": "genre_id", "name": "genre_name"})

    # Keyword Tables:
    keywords_clean = keywords_table_df.rename(columns={"id": "game_id", "keywords": "keyword_id"})
    keyword_info_clean = keyword_info_table_df.rename(columns={"id": "keyword_id", "slug": "keyword_name"})

    # Platform Tables:
    platforms_clean = platforms_table_df.rename(columns={"id": "game_id", "platforms": "platform_id"})
    platform_info_clean = platform_info_table_df.rename(columns={"id": "platform_id", "name": "platform_name"})

    # Converting unix time to datetime format
    games_clean['first_release_date'] = pd.to_datetime(games_clean['first_release_date'], unit='s', origin='unix')

    return {'games': games_clean, 'genres': genres_clean, 'keywords': keywords_clean, 'platforms': platforms_clean,
            'genre_info': genre_info_clean, 'keyword_info': keyword_info_clean, 'platform_info': platform_info_clean}


def store_data(**context):
    # Grab previous task values
    dfs = context['task_instance'].xcom_pull(task_ids='clean_data')
    games_table_df = dfs['games']
    genres_table_df = dfs['genres']
    genre_info_table_df = dfs['genre_info']
    keywords_table_df = dfs['keywords']
    keyword_info_table_df = dfs['keyword_info']
    platforms_table_df = dfs['platforms']
    platform_info_table_df = dfs['platform_info']

    engine = create_engine(
        f"mysql+pymysql://{Variable.get('USER')}:{Variable.get('PASS')}@{Variable.get('RDS_ENDPOINT')}/igdb"
        .format(host=Variable.get("RDS_ENDPOINT"),
                port=Variable.get("RDS_PORT"),
                user=Variable.get('USER'),
                pw=Variable.get('PASS'),
                ))

    for i in range(len(games_table_df)):
        try:
            games_table_df.iloc[i:i + 1].to_sql(name="games", if_exists='append', con=engine, index=False)
        except exc.IntegrityError as e:
            pass

    for i in range(len(genres_table_df)):
        try:
            genres_table_df.iloc[i:i + 1].to_sql(name="genres", if_exists='append', con=engine, index=False)
        except exc.IntegrityError as e:
            pass

    for i in range(len(keywords_table_df)):
        try:
            keywords_table_df.iloc[i:i + 1].to_sql(name="keywords", if_exists='append', con=engine, index=False)
        except exc.IntegrityError as e:
            pass

    for i in range(len(platforms_table_df)):
        try:
            platforms_table_df.iloc[i:i + 1].to_sql(name="platforms", if_exists='append', con=engine, index=False)
        except exc.IntegrityError as e:
            pass

    genre_info_table_df.to_sql(name="genres_info", if_exists='replace', con=engine, index=False)
    keyword_info_table_df.to_sql(name='keyword_info', if_exists='replace', con=engine, index=False)
    platform_info_table_df.to_sql(name="platform_info", if_exists='replace', con=engine, index=False)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 2, 24)
}

with DAG('IGDB_PIPELINE', default_args=default_args, schedule_interval= timedelta(days=1)) as dag:
    get_token_task = PythonOperator(
        task_id='get_auth_token',
        python_callable=get_auth_token
    )

    get_data_task = PythonOperator(
        task_id='get_api_data',
        python_callable=get_api_data,
    )

    clean_data_task = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data,
    )

    store_data_task = PythonOperator(
        task_id='store_data',
        python_callable=store_data,
    )

    # Set task execution order
    get_token_task >> get_data_task >> clean_data_task >> store_data_task
