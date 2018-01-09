CREATE TABLE if NOT EXISTS Lyrics(
  lyrics TEXT(10000),
  seed_id INT NOT NULL UNIQUE,
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY(id),
  FOREIGN KEY (seed_id) REFERENCES Seed(id)
);

LOAD DATA LOCAL INFILE '/Users/orrbarkat/repos/sql_project/Web scraping/lyrics.csv'
INTO TABLE Lyrics
FIELDS TERMINATED BY ','
ENCLOSED BY '|'
LINES TERMINATED BY '\n';
