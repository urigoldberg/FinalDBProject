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


CREATE TABLE if NOT EXISTS Media(
  artist_db_id INT,
  album_db_id INT,
  song_db_id INT UNIQUE,
  media_url VARCHAR(255) NOT NULL  ,
  artist_id INT,
  album_id INT,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  FOREIGN KEY (album_id) REFERENCES Album(id)
);

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

ALTER TABLE CountryACREATE TABLE if NOT EXISTS Album(
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


CREATE TABLE if NOT EXISTS Media(
  artist_db_id INT,
  album_db_id INT,
  song_db_id INT UNIQUE,
  media_url VARCHAR(255) NOT NULL  ,
  artist_id INT,
  album_id INT,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  FOREIGN KEY (album_id) REFERENCES Album(id)
);

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

SELECT count(*) from CountryArtists;




SELECT artists.name, title, Song.id
FROM Song, artists
WHERE Song.artist_id = artists.id
LIMIT 5;

# create fk for song in media
UPDATE Song
set Song.lyrics = %s
WHERE Song.id = %s;


SELECT  @artist_id := id from artists where LOWER(artists.name) = LOWER('radiohead');
INSERT INTO CountryArtists(name, artist_id)
  SELECT * from (SELECT 'AFGHANISTAN', @artist_id) AS tmp
  WHERE NOT exists(
      SELECT * from CountryArtists
      WHERE CountryArtists.name = 'AFGHANISTAN'
            and CountryArtists.artist_id = @artist_id);

SELECT  @artist_id := id from artists where LOWER(artists.name) = LOWER('Pink Floyd') limit 1;
SET @country := 'AFGHANISTAN';
INSERT INTO CountryArtists(name, artist_id)
  SELECT * from (SELECT @country, @artist_id) AS tmp
  WHERE NOT exists(
      SELECT * from CountryArtists
      WHERE CountryArtists.name = @country
            AND CountryArtists.artist_id = @artist_id
  );


Select * from artists where id = @a;

SET @name := %s;" \
"SET @artist := %s;" \
"INSERT INTO CountryArtists(name, artist_id) " \
"SELECT * FROM (SELECT @name, @artist) AS tmp" \
" WHERE NOT EXISTS (" \
"SELECT name FROM CountryArtists WHERE name = @name and artist_id = @artist" \
") LIMIT 1"rtists ADD UNIQUE unique_index (name, artist_id);





SELECT artists.name, title, Song.id
FROM Song, artists
WHERE Song.artist_id = artists.id
LIMIT 5;

# create fk for song in media
UPDATE Song
set Song.lyrics = %s
WHERE Song.id = %s;


SELECT  @artist_id := id from artists where LOWER(artists.name) = LOWER('radiohead');
INSERT INTO CountryArtists(name, artist_id)
  SELECT * from (SELECT 'AFGHANISTAN', @artist_id) AS tmp
  WHERE NOT exists(
      SELECT * from CountryArtists
      WHERE CountryArtists.name = 'AFGHANISTAN'
            and CountryArtists.artist_id = @artist_id);

SELECT  @artist_id := id from artists where LOWER(artists.name) = LOWER('Pink Floyd') limit 1;
SET @country := 'AFGHANISTAN';
INSERT INTO CountryArtists(name, artist_id)
  SELECT * from (SELECT @country, @artist_id) AS tmp
  WHERE NOT exists(
      SELECT * from CountryArtists
      WHERE CountryArtists.name = @country
            AND CountryArtists.artist_id = @artist_id
  );


Select * from artists where id = @a;

SET @name := %s;" \
"SET @artist := %s;" \
"INSERT INTO CountryArtists(name, artist_id) " \
"SELECT * FROM (SELECT @name, @artist) AS tmp" \
" WHERE NOT EXISTS (" \
"SELECT name FROM CountryArtists WHERE name = @name and artist_id = @artist" \
") LIMIT 1"

CREATE TABLE if NOT EXISTS Country(
  name VARCHAR(255) UNIQUE NOT NULL,
  latitude DOUBLE,
  longitude DOUBLE,
  region VARCHAR(255),
  subregion VARCHAR(255),
  capital VARCHAR(255),
  cca3 VARCHAR(3),
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  INDEX lat(latitude),
  INDEX lon(longitude)
);

DROP TABLE Lyrics;
