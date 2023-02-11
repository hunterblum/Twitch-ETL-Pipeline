# ADS507-Practical-Data-Engineering

# Title: 

## Team members: 
-Hunter Blum 

-Ivan Chavez

-Andrew Kim

## Objective: 
The goal of this project is to build and process an ETL pipeline to generate the top video games for users.
Description of dataset: The data set was acquired by using Twitch API, which required authenticating as a Twitch Developer with Oauth2 before posting a request https://id.twitch.tv/oauth2/token and adding client_id, client_secret, and grant_type=client_credentials with the request. The base URL is: https://api.igdb.com/v4, where the token_type as bearer and access_token were also included to the request. Once the access requests were fulfilled, the body of the request was used to specify the fields to retrieve. All actions to access the data set and tables were made through Python.

Attribute information: The following attributes are ones used for our final analysis.
1.	Games.
2.	Genres.
3.	Keywords.
4.	Platforms.
5.	Genres Endpoint.
6.	Keyword Endpoint.
7.	Platform Endpoint.

## Methods:

## Programming Language/Technologies: 
Python and SQL.
