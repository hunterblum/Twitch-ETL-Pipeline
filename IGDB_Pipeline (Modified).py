# %% [markdown]
# # Section 1: Pulling data from API Endpoints/Cleaning

# %%
import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import exc
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

# %%
load_dotenv('.env.txt')

# %%
auth_url = 'https://id.twitch.tv/oauth2/token'
cred = {
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
    'grant_type':'client_credentials'
        }

# %%
r = requests.post(auth_url, data=cred)
data = r.json()
print('Bearer' + data['access_token'])

base_url = 'https://api.igdb.com/v4'
header = {'Client-ID': os.getenv('CLIENT_ID'), 
          'Authorization': 'Bearer ' + data['access_token']}

# %% [markdown]
# # Games Endpoint
# 
# ## Games Table

# %%
#Set max games to pull
max_games = 5000

# %%
i = 0
games_table_df = pd.DataFrame()
while i < max_games/500:
    read = '''fields name, category, first_release_date, status,
            aggregated_rating, aggregated_rating_count, rating, rating_count,
            total_rating, total_rating_count; where category = 0; limit 500; offset '''
    offset = str(500*i)
    semi = ';'
    data = read + offset + semi
    r = requests.post(base_url+'/games', headers=header,
    data= data)
    games_table = r.json()
    games_table_temp = pd.DataFrame(games_table)
    games_table_df=pd.concat([games_table_temp,games_table_df])
    i +=1

# %%
games_table_df

# %% [markdown]
# # Genres Table

# %%
i = 0
genres_table_df = pd.DataFrame()
while i < max_games/500:
    read = 'fields genres; limit 500; offset '
    offset = str(500*i)
    semi = ';'
    data = read + offset + semi
    r = requests.post(base_url+'/games', headers=header,
    data= data)
    genres_table = r.json()
    genres_table_temp =pd.DataFrame(genres_table).explode('genres')
    genres_table_df=pd.concat([genres_table_df,genres_table_temp])
    i +=1

# %%
genres_table_df

# %% [markdown]
# # Keywords Table

# %%
i = 0
keywords_table_df = pd.DataFrame()
while i < max_games/500:
    read = 'fields keywords; limit 500; offset '
    offset = str(500*i)
    semi = ';'
    data = read + offset + semi
    r = requests.post(base_url+'/games', headers=header,
    data= data)
    keywords_table = r.json()
    keywords_table_temp =pd.DataFrame(keywords_table).explode('keywords')
    keywords_table_df=pd.concat([keywords_table_df,keywords_table_temp])
    i +=1

# %%
keywords_table_df

# %% [markdown]
# # Platforms Table

# %%
i = 0
platforms_table_df = pd.DataFrame()
while i < max_games/500:
    read = 'fields platforms; limit 500; offset '
    offset = str(500*i)
    semi = ';'
    data = read + offset + semi
    r = requests.post(base_url+'/games', headers=header,
    data= data)
    platforms_table = r.json()
    platforms_table_temp =pd.DataFrame(platforms_table).explode('platforms')
    platforms_table_df=pd.concat([platforms_table_df,platforms_table_temp])
    i +=1

# %%
platforms_table_df

# %% [markdown]
# # Genres Endpoint
# 
# ## Genres_info Table

# %%
r = requests.post(base_url+'/genres', headers=header, data='fields name; limit 500;')
genre_info_table = r.json()
genre_info_table_df = pd.DataFrame(genre_info_table)
genre_info_table_df

# %% [markdown]
# # Keyword Endpoint
# 
# ## Keyword_info Table

# %%
max_keywords = 10_000
i = 0
keywords_info_table_df = pd.DataFrame()
while i < max_keywords/500:
    read = 'fields slug; limit 500; offset '
    offset = str(500*i)
    semi = ';'
    data = read + offset + semi
    r = requests.post(base_url+'/keywords', headers=header,
    data= data)
    keywords_info_table = r.json()
    keywords_info_table_temp =pd.DataFrame(keywords_info_table)
    keywords_info_table_df=pd.concat([keywords_info_table_df,keywords_info_table_temp])
    i +=1

# %%
keywords_info_table_df

# %% [markdown]
# # Platform Endpoint
# 
# ## Platform Table

# %%
r = requests.post(base_url+'/platforms', headers=header, data='fields name; limit 500;')
platform_info_table = r.json()
platform_info_table_df = pd.DataFrame(platform_info_table)
platform_info_table_df

# %% [markdown]
# # Section 2: Clean/Format Data

# %%
# Renaming df tables to sync with DB Schema
# Games Table:
games_table_df = games_table_df.rename(columns={"id":"game_id"})

# Genre Tables:
genres_table_df = genres_table_df.rename(columns={"id":"game_id", "genres":"genre_id"})
genre_info_table_df = genre_info_table_df.rename(columns={"id":"genre_id", "name":"genre_name"})

# Keyword Tables:
keywords_table_df = keywords_table_df.rename(columns={"id":"game_id", "keywords":"keyword_id"})
keywords_info_table_df = keywords_info_table_df.rename(columns={"id":"keyword_id", "slug":"keyword_name"})

# Platform Tables:
platforms_table_df = platforms_table_df.rename(columns={"id":"game_id", "platforms":"platform_id"})
platform_info_table_df = platform_info_table_df.rename(columns={"id":"platform_id", "name":"platform_name"})

# %%
# Converting unix time to datetime format
games_table_df['first_release_date'] = pd.to_datetime(games_table_df['first_release_date'], unit='s', origin='unix')

# %% [markdown]
# # Section 3: Upload to AWS RDS MySQL Server

# %%
engine = create_engine(f"mysql+pymysql://{os.getenv('USER')}:{os.getenv('PASSWORD')}@{os.getenv('RDS_ENDPOINT')}/igdb"
                       .format(host= os.getenv("RDS_ENDPOINT"),
                               port= os.getenv("RDS_PORT"),
                               user=os.getenv('USER'),
                               pw=os.getenv('PASSWORD'),
                               ))

# %%
for i in range(len(games_table_df)):
    try:
        games_table_df.iloc[i:i+1].to_sql(name="games",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

# %%
for i in range(len(genres_table_df)):
    try:
        genres_table_df.iloc[i:i+1].to_sql(name="genres",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

# %%
for i in range(len(keywords_table_df)):
    try:
        keywords_table_df.iloc[i:i+1].to_sql(name="keywords",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

# %%
for i in range(len(platforms_table_df)):
    try:
        platforms_table_df.iloc[i:i+1].to_sql(name="platforms",if_exists='append',con = engine, index=False)
    except exc.IntegrityError as e:
        pass

# %%
genre_info_table_df.to_sql(name="genres_info",if_exists='replace', con = engine, index=False)
keywords_info_table_df.to_sql(name='keyword_info',if_exists='replace', con= engine, index=False)
platform_info_table_df.to_sql(name="platform_info", if_exists='replace', con= engine, index=False)

# %% [markdown]
# # Section 4 - Example Queries and Plots
# 
# ## Top Rated Tables by Game Rating

# %%
# Genres with top rated games
query_top10_genre = """SELECT gni.genre_name, AVG(gm.rating) AS avg_rating
                    FROM games AS gm
                    INNER JOIN genres AS gn ON gm.game_id = gn.game_id
                    INNER JOIN genres_info AS gni ON gn.genre_id = gni.genre_id
                    GROUP BY gni.genre_id
                    ORDER BY avg_rating DESC
                    LIMIT 10;"""
Query_Top10_Genre = pd.read_sql_query(sql=text(query_top10_genre), con=engine.connect())
Query_Top10_Genre

# %%
Query_Top10_Genre = Query_Top10_Genre.sort_values(by=['avg_rating'])
Genre = Query_Top10_Genre['genre_name']
Average_Rating = Query_Top10_Genre['avg_rating']

plt.barh(y=Genre, width=Average_Rating)
plt.xlabel("Average Rating", fontsize = 12)
plt.ylabel("Genre", fontsize = 12)
plt.title("Figure X.x: Top User Rated Genres", fontsize = 14)
plt.show()

# %%
# Keywords with top rated games, where key word appears at least 5 times.
query_top10_keyword="""SELECT ki.keyword_name, AVG(gm.rating) AS avg_rating
                    FROM games AS gm
                    INNER JOIN keywords AS k ON gm.game_id = k.game_id
                    INNER JOIN keyword_info AS ki ON k.keyword_id = ki.keyword_id
                    GROUP BY ki.keyword_id
                    HAVING COUNT(ki.keyword_id)>4
                    ORDER BY avg_rating DESC
                    LIMIT 10;"""
Query_Top10_Keyword = pd.read_sql_query(sql=text(query_top10_keyword), con=engine.connect())
Query_Top10_Keyword

# %%
Query_Top10_Keyword = Query_Top10_Keyword.sort_values(by=['avg_rating'])
Keyword = Query_Top10_Keyword['keyword_name']
Average_Rating = Query_Top10_Keyword['avg_rating']

plt.barh(y=Keyword, width=Average_Rating)
plt.xlabel("Average Rating", fontsize = 12)
plt.ylabel("Keyword", fontsize = 12)
plt.title("Figure X.x: Top User Rated Keywords", fontsize = 14)
plt.show()

# %%
# Platforms with top rated games, where platform has at least 25 games
query_top10_platforms = """SELECT pi.platform_name, AVG(gm.rating) AS avg_rating
                            FROM games AS gm
                            INNER JOIN platforms AS p ON gm.game_id = p.game_id
                            INNER JOIN platform_info AS pi ON p.platform_id = pi.platform_id
                            GROUP BY pi.platform_id
                            HAVING COUNT(pi.platform_id)>24
                            ORDER BY avg_rating DESC
                            LIMIT 10;"""
Query_Top10_Platforms = pd.read_sql_query(sql=text(query_top10_platforms), con=engine.connect())
Query_Top10_Platforms

# %%
Query_Top10_Platforms = Query_Top10_Platforms.sort_values(by=['avg_rating'])
Platform = Query_Top10_Platforms['platform_name']
Average_Rating = Query_Top10_Platforms['avg_rating']

plt.barh(y=Platform, width=Average_Rating)
plt.xlabel("Average Rating", fontsize = 12)
plt.ylabel("Platform", fontsize = 12)
plt.title("Figure X.x: Top User Rated Platforms", fontsize = 14)
plt.show()

# %% [markdown]
# ## What games have the biggest difference between audience and critic score?

# %%
# Games IGDB users liked better for games with at least 10 reviews.
query_score_diff = """SELECT name, rating AS user_rating, aggregated_rating AS critic_rating, 
                    rating-aggregated_rating AS rating_diff
                    FROM games
                    WHERE rating_count>4 AND aggregated_rating_count>4
                    AND rating-aggregated_rating>0
                    ORDER BY rating_diff DESC
                    LIMIT 10;"""
Query_Score_Diff_user = pd.read_sql_query(sql=text(query_score_diff), con=engine.connect())
Query_Score_Diff_user

# %%
barwidth = 0.25
Query_Score_Diff_user = Query_Score_Diff_user.sort_values(by=['rating_diff'])
Game = Query_Score_Diff_user['name']
Game_axis = np.arange(len(Game))
Rating_diff = Query_Score_Diff_user['rating_diff']
User_rating = Query_Score_Diff_user['user_rating']
Critic_rating = Query_Score_Diff_user['critic_rating']

bar1 = plt.barh(y=Game_axis- .2, width= User_rating, label = 'User Rating', height = 0.3, color = "Black")
bar2 = plt.barh(y=Game_axis + .2, width=Critic_rating, label = 'Critic Rating', height= 0.3, color = "Grey")
plt.yticks(Game_axis, Game)
plt.xlabel("Average Rating", fontsize = 12)
plt.ylabel("Game", fontsize = 12)
plt.title("Figure X.x: Games Users Liked More than Critics", fontsize = 14)
plt.legend( (bar1, bar2), ('User', 'Critic'))
plt.show()

# %%
# Games critics liked more than users
query_score_diff = """SELECT name, rating AS user_rating, aggregated_rating AS critic_rating, 
                    aggregated_rating-rating AS rating_diff
                    FROM games
                    WHERE rating_count>4 AND aggregated_rating_count>4
                    AND aggregated_rating-rating>0
                    ORDER BY rating_diff DESC
                    LIMIT 10;"""
Query_Score_Diff_crit = pd.read_sql_query(sql=text(query_score_diff), con=engine.connect())
Query_Score_Diff_crit

# %%
barwidth = 0.25
Query_Score_Diff_crit = Query_Score_Diff_crit.sort_values(by=['rating_diff'])
Game = Query_Score_Diff_crit['name']
Game_axis = np.arange(len(Game))
Rating_diff = Query_Score_Diff_crit['rating_diff']
User_rating = Query_Score_Diff_crit['user_rating']
Critic_rating = Query_Score_Diff_crit['critic_rating']

bar1 = plt.barh(y=Game_axis- .2, width= User_rating, label = 'User Rating', height = 0.3, color = "Black")
bar2 = plt.barh(y=Game_axis + .2, width=Critic_rating, label = 'Critic Rating', height= 0.3, color = "Grey")
plt.yticks(Game_axis, Game)
plt.xlabel("Average Rating", fontsize = 12)
plt.ylabel("Game", fontsize = 12)
plt.title("Figure X.x: Games Critics Liked More than Users", fontsize = 14)
plt.legend( (bar1, bar2), ('User', 'Critic'))
plt.show()


