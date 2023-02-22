#DROP DATABASE `igdb`;
CREATE SCHEMA `igdb` ;
USE igdb;


# Endpoint - Games
CREATE TABLE games
(game_id INT,
game_name VARCHAR(100),
category INT,
release_date DATE,
game_status INT,
crtic_rating INT,
critic_rating_count INT,
user_rating INT,
user_rating_count INT, 
total_rating INT,
total_rating_count INT,
PRIMARY KEY (game_id)
);

# Endpoint - Games
CREATE TABLE genres
(genre_key INT UNSIGNED,
genre INT,
game_id INT,
PRIMARY KEY (genre_key),
FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Genres
CREATE TABLE genres_info
(genre INT,
genre_name VARCHAR(50),
PRIMARY KEY (genre)
);

# Endpoint - Games
CREATE TABLE keywords
(keyword_key INT UNSIGNED,
keyword INT,
game_id INT,
PRIMARY KEY (keyword_key),
FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Keyword
CREATE TABLE keyword_info
(keyword INT,
keyword_name VARCHAR(50),
PRIMARY KEY (keyword)
);

# Endpoint - Game
CREATE TABLE platforms
(platform_key INT UNSIGNED,
platform INT,
game_id INT, 
PRIMARY KEY (platform_key),
FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Platform
CREATE TABLE platform_info
(platform INT,
platform_name VARCHAR(20),
PRIMARY KEY (platform)
);






# Kept for possible future use
#CREATE TABLE age_ratings_info
#(age_rating INT,
#category VARCHAR(20),
#rating VARCHAR(20),
#PRIMARY KEY (age_rating)
#);

#CREATE TABLE age_ratings
#(rating_id INT UNSIGNED,
#age_rating INT,
#game_id INT,
#PRIMARY KEY (rating_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

#CREATE TABLE characters
#(character_id INT,
#game_id INT,
#character_name VARCHAR(100),
#PRIMARY KEY (character_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

#CREATE TABLE collections
#(collection_id  INT,
#game_id INT,
#collection_name VARCHAR(100),
#PRIMARY KEY (collection_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

#CREATE TABLE companies
#(company_id  INT,
#game_id  INT, 
#company_name VARCHAR(100),
#PRIMARY KEY (company_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

#CREATE TABLE franchises
#(franchise_id INT,
#game_id INT, 
#franchise_name VARCHAR(100),
#PRIMARY KEY (franchise_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

#CREATE TABLE game_modes_info
#(game_mode INT, 
#mode_name VARCHAR(50),
#PRIMARY KEY (game_mode)
#);


#CREATE TABLE game_modes
#(mode_id INT UNSIGNED,
#game_mode INT,
#game_id INT,
#PRIMARY KEY (mode_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

# Endpoint - Games
#CREATE TABLE themes 
#(theme INT, 
#game_id INT,
#PRIMARY KEY (theme),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);

# Endpoint - Themes
#CREATE TABLE theme_info
#(theme INT,
#theme_name VARCHAR(20),
#PRIMARY KEY (theme),
#FOREIGN KEY (theme) REFERENCES themes(theme)
#);

#CREATE TABLE websites
#(website_id INT,
#category INT,
#game_id INT,
#url VARCHAR(200),
#PRIMARY KEY (website_id),
#FOREIGN KEY (game_id) REFERENCES games(game_id)
#);