CREATE DATABASE if NOT EXISTS DbMysql12;
use DbMysql12;

create table if NOT EXISTS Artist(
  id int not null auto_increment
    primary key,
  db_id int not null,
  name varchar(128) not null,
  label varchar(128) ,
  formed_year int ,
  year_of_birth int,
  year_of_death int,
  disbanded varchar(5),
  mood varchar(45),
  style varchar(45),
  genre varchar(45),
  website varchar(128),
  facebook varchar(128),
  twitter varchar(128),
  biography varchar(4096),
  gender varchar(16),
  members int,
  location varchar(45),
  image varchar(128),
  logo varchar(128),
  constraint id_UNIQUE
  unique (id),
  constraint db_id_UNIQUE
  unique (db_id)
);

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

CREATE TABLE if NOT EXISTS Lyrics(
  lyrics TEXT,
  song_id INT UNIQUE,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FULLTEXT (lyrics)
)ENGINE = MYISAM;

CREATE TABLE if NOT EXISTS Song(
  db_id INT NOT NULL UNIQUE,
  artist_db_id INT,
  album_db_id INT,
  title VARCHAR(128) NOT NULL,
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

CREATE TABLE if NOT EXISTS CountryArtists(
  name VARCHAR(255),
  artist_id INT NOT NULL,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  FOREIGN KEY (name) REFERENCES Country(name),
  INDEX CountryArtists(name) USING BTREE,
  UNIQUE unique_index (name, artist_id)
);

CREATE TABLE if NOT EXISTS users_table(
  user_name VARCHAR(21) NOT NULL UNIQUE,
  password VARCHAR(21) UNIQUE,
  birth_year YEAR(4),
  long_songs_lover INT,
  genre VARCHAR(128),
  counrty VARCHAR(128),
  PRIMARY KEY(user_name)
);

CREATE TABLE if NOT EXISTS UserInteraction(
  user_name VARCHAR(20),
  song_id INT,
  created_at TIMESTAMP,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  FOREIGN KEY (user_name) REFERENCES users_table(user_name),
  FOREIGN KEY (song_id) REFERENCES Song(id),
  UNIQUE (user_name, song_id),
  INDEX (user_name)
);