-- Drop existing tables if they exist to avoid conflicts
DROP TABLE IF EXISTS song_album;
DROP TABLE IF EXISTS song_credits;
DROP TABLE IF EXISTS setlist_songs;
DROP TABLE IF EXISTS setlists;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS tours;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS master_songs;

-- Master Songs Table (new)
CREATE TABLE master_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
);

-- Songs Table (updated)
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    master_song_id INT,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    discogs_id INT UNIQUE,
    duration INT,
    UNIQUE (title, release_date),
    FOREIGN KEY (master_song_id) REFERENCES master_songs(id) ON DELETE CASCADE
);

-- Albums Table
CREATE TABLE albums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    release_year YEAR,
    discogs_id INT UNIQUE,
    format VARCHAR(255), -- Added column for album format
    notes TEXT
);

-- People Table
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100),
    notes TEXT
);

-- Song Credits Table (Writers, Producers, etc.)
CREATE TABLE song_credits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT,
    person_id INT,
    role VARCHAR(100), -- e.g., Producer, Writer, Director
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
);

-- Tours Table
CREATE TABLE IF NOT EXISTS tours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE
);

-- Venues Table
CREATE TABLE IF NOT EXISTS venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    other TEXT
);

-- Setlists Table
CREATE TABLE IF NOT EXISTS setlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id INT,
    venue_id INT,
    event_date DATE NOT NULL, -- Ensure this column is defined correctly
    event_name VARCHAR(255),
    notes TEXT,
    approximate_date BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (tour_id) REFERENCES tours(id),
    FOREIGN KEY (venue_id) REFERENCES venues(id)
);

-- Relationship: Songs ↔ Albums (Many-to-Many)
CREATE TABLE IF NOT EXISTS song_album (
    song_id INT,
    album_id INT,
    PRIMARY KEY (song_id, album_id),
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);

-- Relationship: Setlists ↔ Songs (Many-to-Many with song order)
CREATE TABLE IF NOT EXISTS setlist_songs (
    setlist_id INT,
    song_id INT,
    song_order INT,
    PRIMARY KEY (setlist_id, song_id),
    FOREIGN KEY (setlist_id) REFERENCES setlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Master Releases Table (Discogs)
CREATE TABLE master_releases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year YEAR,
    discogs_id INT UNIQUE,
    notes TEXT
);

-- Individual Releases (Versions) Table
CREATE TABLE versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    master_release_id INT,
    title VARCHAR(255) NOT NULL,
    format VARCHAR(255),
    label VARCHAR(255),
    country VARCHAR(100),
    release_date DATE,
    discogs_id INT UNIQUE,
    notes TEXT,
    FOREIGN KEY (master_release_id) REFERENCES master_releases(id) ON DELETE CASCADE
);

-- Release Tracks Table
CREATE TABLE IF NOT EXISTS release_tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    release_id INT,
    song_id INT,
    track_number INT,
    title VARCHAR(255) NOT NULL,
    duration INT,
    FOREIGN KEY (release_id) REFERENCES versions(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Release Credits Table
CREATE TABLE release_credits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    release_id INT,
    person_id INT,
    role VARCHAR(100), -- e.g., Producer, Writer, Mixer
    FOREIGN KEY (release_id) REFERENCES versions(id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
);

-- Release Images Table
CREATE TABLE release_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    release_id INT,
    image_url TEXT,
    FOREIGN KEY (release_id) REFERENCES versions(id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_song_album_album_id ON song_album(album_id);
CREATE INDEX idx_setlist_songs_song_id ON setlist_songs(song_id);
CREATE INDEX idx_people_name ON people(name);

-- Indexes for faster lookups
CREATE INDEX idx_master_release_id ON versions(master_release_id);
CREATE INDEX idx_release_tracks_release_id ON release_tracks(release_id);
CREATE INDEX idx_release_credits_release_id ON release_credits(release_id);
CREATE INDEX idx_release_images_release_id ON release_images(release_id);

SET AUTOCOMMIT = 1;