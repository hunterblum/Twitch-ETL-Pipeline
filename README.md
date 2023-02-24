# ADS507-Practical-Data-Engineering

# Title: TBD

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

## Programming Language/Technologies: 
Python through Jupyter Notebook within VS Code, MySQLWorkbench, Amazon Web Services RDS application, Apache Airflow.
