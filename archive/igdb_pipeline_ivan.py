import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy import exc
from dotenv import load_dotenv

load_dotenv()


auth_url = 'https://id.twitch.tv/oauth2/token'
cred = {'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type':'client_credentials'}
r = requests.post(auth_url, data=cred)
data = r.json()

base_url = 'https://api.igdb.com/v4'
header = {'Client-ID': os.getenv('CLIENT_ID'),
          'Authorization': 'Bearer '+data['access_token']}

r = requests.post(base_url+'/games', headers=header,
                  data='''fields name, category, first_release_date, status,
aggregated_rating, aggregated_rating_count, rating, rating_count,
total_rating, total_rating_count; where category = 0; limit 100;''')
games_table = r.json()
games_table_df = pd.DataFrame(games_table)

r = requests.post(base_url+'/games', headers=header,
                  data='fields genres; limit 100;')
genres_table = r.json()
genres_table_df =pd.DataFrame(genres_table).explode('genres')

r = requests.post(base_url+'/games', headers=header,
                  data='fields keywords; limit 100;')
keywords_table = r.json()
keywords_table_df =pd.DataFrame(keywords_table).explode('keywords')

r = requests.post(base_url+'/games', headers=header,
                  data='fields platforms; limit 100;')
platforms_table = r.json()
platforms_table_df =pd.DataFrame(platforms_table).explode('platforms')

r = requests.post(base_url+'/genres', headers=header, data='fields name; limit 500;')
genre_info_table = r.json()
genre_info_table_df = pd.DataFrame(genre_info_table)

r = requests.post(base_url+'/keywords', headers=header, data='fields slug; limit 100;')
keyword_info_table = r.json()
keyword_info_table_df = pd.DataFrame(keyword_info_table)

r = requests.post(base_url+'/platforms', headers=header, data='fields name; limit 100;')
platform_info_table = r.json()
platform_info_table_df = pd.DataFrame(platform_info_table)

# Renaming df tables to sync with DB Schema
# Games Table:
games_table_df = games_table_df.rename(columns={"id":"game_id"})

# Genre Tables:
genres_table_df = genres_table_df.rename(columns={"id":"game_id", "genres":"genre_id"})
genre_info_table_df = genre_info_table_df.rename(columns={"id":"genre_id", "name":"genre_name"})

# Keyword Tables:
keywords_table_df = keywords_table_df.rename(columns={"id":"game_id", "keywords":"keyword_id"})
keyword_info_table_df = keyword_info_table_df.rename(columns={"id":"keyword_id", "slug":"keyword_name"})

# Platform Tables:
platforms_table_df = platforms_table_df.rename(columns={"id":"game_id", "platforms":"platform_id"})
platform_info_table_df = platform_info_table_df.rename(columns={"id":"platform_id", "name":"platform_name"})

# Converting unix time to datetime format
games_table_df['first_release_date'] = pd.to_datetime(games_table_df['first_release_date'], unit='s', origin='unix')

engine = create_engine(f"mysql+pymysql://{os.getenv('USER')}:{os.getenv('PASS')}@{os.getenv('RDS_ENDPOINT')}/igdb"
                       .format(host= os.getenv("RDS_ENDPOINT"),
                               port= os.getenv("RDS_PORT"),
                               user=os.getenv('USER'),
                               pw=os.getenv('PASS'),
                               ))


for i in range(len(games_table_df)):
    try:
        games_table_df.iloc[i:i+1].to_sql(name="games",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

for i in range(len(genres_table_df)):
    try:
        genres_table_df.iloc[i:i+1].to_sql(name="genres",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

for i in range(len(keywords_table_df)):
    try:
        keywords_table_df.iloc[i:i+1].to_sql(name="keywords",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

for i in range(len(platforms_table_df)):
    try:
        platforms_table_df.iloc[i:i+1].to_sql(name="platforms",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

genre_info_table_df.to_sql(name="genres_info",if_exists='replace', con = engine, index=False)
keyword_info_table_df.to_sql(name='keyword_info',if_exists='replace', con= engine, index=False)
platform_info_table_df.to_sql(name="platform_info", if_exists='replace', con= engine, index=False)

print("Database has been updated!")