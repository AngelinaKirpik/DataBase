CREATE TABLE IF NOT EXISTS Genres(
genre_id SERIAL PRIMARY KEY,
genre_name VARCHAR(50) NOT NULL CHECK (genre_name <> '')
);

CREATE TABLE IF NOT EXISTS Performers(
performer_id SERIAL PRIMARY KEY,
performer_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Albums(
album_id SERIAL PRIMARY KEY,
album_name VARCHAR(50) NOT NULL,
album_year SMALLINT NOT NULL CHECK (album_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE))
);

CREATE TABLE IF NOT EXISTS Tracks(
track_id SERIAL PRIMARY KEY,
track_name VARCHAR(50) NOT NULL,
track_duration INTEGER NOT NULL CHECK (track_duration > 0),
album_id INTEGER NOT NULL REFERENCES Albums(album_id)
);

CREATE TABLE IF NOT EXISTS Compilations(
compilation_id SERIAL PRIMARY KEY,
compilation_name VARCHAR(50) NOT NULL,
compilation_year SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS Genres_Performers(
genre_id INTEGER REFERENCES Genres(genre_id),
performer_id INTEGER REFERENCES Performers(performer_id),
CONSTRAINT pk_genres_performers PRIMARY KEY (genre_id, performer_id)
);

CREATE TABLE IF NOT EXISTS Performers_Albums(
performer_id INTEGER REFERENCES Performers(performer_id),
album_id INTEGER REFERENCES Albums(album_id),
CONSTRAINT pk_performers_albums PRIMARY KEY (performer_id, album_id)
);

CREATE TABLE IF NOT EXISTS Tracks_Compilations(
track_id INTEGER REFERENCES Tracks(track_id),
compilation_id INTEGER REFERENCES Compilations(compilation_id),
CONSTRAINT pk_tracks_compilation PRIMARY KEY (track_id, compilation_id)
);
