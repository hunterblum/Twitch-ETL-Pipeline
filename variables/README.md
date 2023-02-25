# Airflow Variables Guide

A sample structure of the project variables needed to run the dag have been provided in the **airflow-var.json** file. A breakdown of the variables are provided below:<br/> 
* **Client ID & Client Secret** : Corresponds to the Twitch IGDB API Credentials more information on retrieving those credentials can be found [here](https://api-docs.igdb.com/#getting-started)
* **User, Pass, Endpoint, Port**: These all relate to database login credentials, this project utilized a MySQL AWS RDS Instance more information on getting started with AWS RDS can be found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)

## Importing Variables
Once all project field variables have been filled they can be easily imported within the airflow GUI via the following steps:
1. Click on the Admin dropdown menu
2. Click on Variables
3. At the top of the variable menu select the json file with your project variables to import
4. Click Import Variables and the variable grid will populate with your values
