create table if not exists Seed(
  title VARCHAR(255),
  artist_hotttnesss DOUBLE,
  artist_id varchar(255),
  artist_name varchar(255),
  duration DOUBLE,
  familiarity DOUBLE,
  latitude DOUBLE,
  longitude DOUBLE,
  loudness DOUBLE,
  release_id VARCHAR(255),
  release_name VARCHAR(255),
  similar	VARCHAR(255),
  song_hotttnesss	DOUBLE,
  song_id	VARCHAR(255),
  tempo DOUBLE,
  terms VARCHAR(255),
  year YEAR(4),
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id)
);

LOAD DATA LOCAL INFILE '/Users/orrbarkat/repos/sql_project/Web scraping/music.csv'
INTO TABLE Seed
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
