DROP DATABASE `igdb`;
CREATE SCHEMA `igdb` ;
USE igdb;


# Endpoint - Games
CREATE TABLE games
(game_id INT,
 name VARCHAR(100),
 category INT,
 first_release_date DATE,
 status INT,
 rating INT,
 rating_count INT,
 total_rating INT,
 total_rating_count INT,
 aggregated_rating INT,
 aggregated_rating_count INT,
 PRIMARY KEY (game_id)
);

# Endpoint - Games
CREATE TABLE genres
(genres_id INT AUTO_INCREMENT PRIMARY KEY,
 game_id INT,
 genre_id INT,
 FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Games
CREATE TABLE keywords
(keywords_id INT AUTO_INCREMENT PRIMARY KEY,
 game_id INT,
 keyword_id INT,
 FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Game
CREATE TABLE platforms
(platforms_id INT AUTO_INCREMENT PRIMARY KEY,
 game_id INT,
 platform_id INT,
 FOREIGN KEY (game_id) REFERENCES games(game_id)
);

# Endpoint - Genres
CREATE TABLE genres_info
(genre_id INT,
 genre_name VARCHAR(50),
 PRIMARY KEY (genre_id)
);

# Endpoint - Keyword
CREATE TABLE keyword_info
(keyword_id INT,
 keyword_name VARCHAR(50),
 PRIMARY KEY (keyword_id)
);

# Endpoint - Platform
CREATE TABLE platform_info
(platform_id INT,
 platform_name VARCHAR(20),
 PRIMARY KEY (platform_id)
);
