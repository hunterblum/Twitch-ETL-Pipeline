# Down the Warp Pipe: Creating an ETL Pipeline for a Video Game Recommendation System

## Team members: 
-Hunter Blum 

-Ivan Chavez

-Andrew Kim

## Objective: 
The goal of this project is to process and construct a database using ETL pipeline for a rudimentary video game recommender system.

## Description of dataset: 
The data's source came from the IGDB API run by Twitch, which contained over 200,000 unique video games that is continually updated and upgraded and multiple aspects/features of each game. Retrieving the data for our pipeline required authenticating the IGDB API as a Twitch Developer with Oauth2 before posting a request that included a client_id, client_secret, and grant_type=client_credentials with the request. The base URL is: https://api.igdb.com/v4, where the token_type as bearer and access_token were also included to the request. Once the access requests were fulfilled, the body of the request was used to specify the fields to retrieve, which we used MySQL Workbench and Python through Jupyter Notebook within VSCode to clean and extract the necessary data.

## Attribute information: The following attributes are ones used for our final analysis.
1.	Games.
2.	Genres.
3.	Keywords.
4.	Platforms.
5.	Genres Endpoint.
6.	Keyword Endpoint.
7.	Platform Endpoint.

## Methods: 
A schema using MySQL Workbench was created to match the endpoints in the API. The required data from the API was then extracted through Python using Jupyter Notebook within VSCode before the coding process using Jupyter Notebook was cleaned and migrated into a python file to extract the necessary api data into a shared RDS database. Once the data was migrated into a single server, queries that analyzed games that were highly ranked based on key features and were surveyed between users and reviewers were generated.  Visualizations (i.e.: bar charts) in Python were also created to support the queries. Lastly, the process was automated using Apache Airflow.

## How to deploy pipeline
**Assumes Docker Daemon is running**
1. Clone repository
2. Open repository directory in command line or terminal
3. Run the following command inside the project root: <code> docker-compose up </code>
<br>*Note: Takes a couple minutes for Airflow to start up*
5. Access local Airflow instance via default URL (http://localhost:8080/)
5. Login using default credentials:
   * Username: airflow
   * Password: airflow
6. Import project variables more information [here](variables/README.md) 
7. Click the green play button for **IGDB_PIPELINE** to manually start the pipeline


## Programming Language/Technologies: 
Python through Jupyter Notebook within VS Code, MySQLWorkbench, Amazon Web Services RDS application, Apache Airflow.

## Appendix: Description of Elements within each Table
### Games Table
-game_id INT: The primary key for the table.

-name VARCHAR(100): The name of the video game

-category INT: Is the game the main game, dlc, bundle, etc? Filtered for main games only currently

-first_release_date DATE: The first release date for the title

-status INT: Is the game released, in alpha testing, canceled, etc?

-rating INT: Average IGDB user rating for the game

-rating_count INT: Number of IGDB user ratings for the game

-total_rating INT: Average critic rating for the game

-total_rating_count INT: Number of critic ratings for the game

-aggregated_rating INT: Combined user and critic ratings for the game

-aggregated_rating_count INT: Number of aggregated ratings for the game


### Genres Table
-genres_id INT: The primary key for the table

-game_id INT: A foreign key constraint connected to the games table

-genre_id INT: The genre code for the game

### Genres_info Table
-genre_id BIGINT: The genre code for the game

-genre_name TEXT: The textual name for the genre

### Keywords Table
-keywords_id INT: The primary key for the table

-game_id INT: A foreign key constraint connected to the games table

-keyword_id INT: The keyword code for the game

### Keywords_info Table
-keyword_id BIGINT: The keyword code for the game

-keyword_name TEXT: The textual name for the keyword

### Platforms Table
-platforms_id INT: The primary key for the table

-game_id INT: A foreign key constraint connected to the games table

-platform_id INT: The platform code for the game

### Platforms_info Table
-platform_id BIGINT: The platform code for the game

-platform_name TEXT: The textual name for the platform

