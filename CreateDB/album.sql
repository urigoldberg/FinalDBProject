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
  song_db_id INT,
  media_url VARCHAR(255) UNIQUE NOT NULL,
  song_id INT,
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
  lyrics_id INT,
  media_id INT,
  title VARCHAR(128),
  genre VARCHAR(128),
  description TEXT(4096),
  artist_id INT,
  album_id INT,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (artist_id) REFERENCES artists(id),
  FOREIGN KEY (album_id) REFERENCES Album(id),
  FOREIGN KEY (media_id) REFERENCES Media(id)
);

# create fk for song in media
UPDATE Song
set media_id = (SELECT Media.id FROM Media, Song WHERE Song.db_id = Media.song_db_id)
WHERE Song.id is NULL
      AND EXISTS(SELECT Media.id FROM Media, Song WHERE Song.db_id = Media.song_db_id);