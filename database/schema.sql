-- Drop tables if they exist
DROP TABLE IF EXISTS song_credits;
DROP TABLE IF EXISTS song_album;
DROP TABLE IF EXISTS setlist_songs;
DROP TABLE IF EXISTS setlists;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS tours;
DROP TABLE IF EXISTS venues;

-- Songs Table
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    duration INT, -- In seconds
    discogs_id INT UNIQUE, -- Matches Discogs data
    is_single BOOLEAN DEFAULT FALSE
);

-- Albums Table
CREATE TABLE albums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    discogs_id INT UNIQUE
);

-- Relationship: Songs ↔ Albums (Many-to-Many)
CREATE TABLE song_album (
    song_id INT,
    album_id INT,
    PRIMARY KEY (song_id, album_id),
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);

-- Song Credits Table (Writers, Producers, etc.)
CREATE TABLE song_credits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT,
    contributor_name VARCHAR(255),
    role VARCHAR(50), -- "Writer", "Producer", etc.
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Tours Table
CREATE TABLE tours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Venues Table
CREATE TABLE venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    country VARCHAR(255),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

-- Setlists Table (Each concert performance)
CREATE TABLE setlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id INT,
    venue_id INT,
    event_date DATE NOT NULL,
    FOREIGN KEY (tour_id) REFERENCES tours(id) ON DELETE SET NULL,
    FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE SET NULL
);

-- Relationship: Setlists ↔ Songs (Many-to-Many)
CREATE TABLE setlist_songs (
    setlist_id INT,
    song_id INT,
    position INT, -- Order in the performance
    PRIMARY KEY (setlist_id, song_id),
    FOREIGN KEY (setlist_id) REFERENCES setlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);