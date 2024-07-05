-- SQLite3 database schema

CREATE TABLE votes (
  id      INTEGER PRIMARY KEY NOT NULL,
  key     TEXT NOT NULL UNIQUE,
  mod     TEXT NOT NULL,
  title   TEXT NOT NULL,
  closing INTEGER NOT NULL,
  expiry  INTEGER NOT NULL
);

CREATE UNIQUE INDEX idx_votes_key ON votes(key);

CREATE TABLE propositions (
  id    INTEGER PRIMARY KEY NOT NULL,
  vote  INTEGER NOT NULL,
  title TEXT NOT NULL,
  score TEXT NOT NULL,
  FOREIGN KEY (vote) REFERENCES votes(id)
);

CREATE TABLE ballots (
  id          INTEGER PRIMARY KEY NOT NULL,
  vote        INTEGER NOT NULL,
  author      TEXT NOT NULL,
  checksum    TEXT NOT NULL,
  fingerprint TEXT NOT NULL,
  FOREIGN KEY (vote) REFERENCES votes(id)
);

CREATE TABLE entries (
  ballot      INTEGER NOT NULL,
  proposition INTEGER NOT NULL,
  entry       TEXT NOT NULL,
  FOREIGN KEY (ballot) REFERENCES ballots(id)
  FOREIGN KEY (proposition) REFERENCES propositions(id)
);
