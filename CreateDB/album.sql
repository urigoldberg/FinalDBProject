CREATE TABLE if NOT EXISTS Album(
  db_id INT NOT NULL UNIQUE,
  artist_db_id INT,
  name VARCHAR(128),
  release_year YEAR(4),
  style VARCHAR(128),
  genre VARCHAR(128),
  sales INT,
  thumb_url VARCHAR(255),
  Album_art_url VARCHAR(255),
  description TEXT(4096),
  score INT,
  votes INT,
  artist_id INT,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id)
);

# CREATE TABLE if NOT EXISTS Media(
#   artist_db_id INT,
#   album_db_id INT,
#   song_db_id INT UNIQUE,
#   media_url VARCHAR(255) NOT NULL  ,
#   artist_id INT,
#   album_id INT,
#   id INT NOT NULL AUTO_INCREMENT,
#   PRIMARY KEY(id),
#   FOREIGN KEY (artist_id) REFERENCES artists(id),
#   FOREIGN KEY (album_id) REFERENCES Album(id)
# );

CREATE TABLE if NOT EXISTS Song(
  db_id INT NOT NULL UNIQUE,
  artist_db_id INT,
  album_db_id INT,
  lyrics TEXT(5000),
  title VARCHAR(128) NOT NULL ,
  duration TEXT(4096),
  genre VARCHAR(128),
  media_url VARCHAR(255),
  media_views INT,
  media_likes INT,
  order_in_album INT,
  score int,
  score_votes int,
  artist_id INT,
  album_id INT,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  FOREIGN KEY (album_id) REFERENCES Album(id)
);

CREATE TABLE if NOT EXISTS CountryArtists(
  name VARCHAR(255),
  artist_id INT NOT NULL,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  INDEX CountryArtists(name) USING BTREE,
  UNIQUE unique_index (name, artist_id)
);
