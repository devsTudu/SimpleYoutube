-- Active: 1754881684234@@127.0.0.1@3306
CREATE TABLE Activity(  
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    searchTerm TEXT,
    course_id TEXT,
    lesson_id TEXT,
    note_id TEXT,
    comments TEXT NOT NULL
);

CREATE Table videoInfo(
    video_id TEXT PRIMARY KEY,
    completedOn DATETIME,
    startedOn DATETIME,
    videoTitle TEXT NOT NULL,
    videoDescr TEXT,
    channel_id TEXT,
    thumbnail_url TEXT
)

CREATE TABLE Notes(
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT NOT NULL,
    takenOn DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastUpdated DATETIME,
    notes_content TEXT
);

CREATE TABLE Playlists(
    pl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlistid TEXT UNIQUE NOT NULL,
    playlistName TEXT NOT NULL,
    total_videos UNSIGNED INTEGER DEFAULT 0,
    channel_id TEXT,
    lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE Playlist_Video_Junction (
    playlist_id TEXT,
    video_id TEXT,
    PRIMARY KEY (playlist_id, video_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlistid),
    FOREIGN KEY (video_id) REFERENCES videoInfo(video_id)
);

CREATE TABLE channel(
    channel_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    views UNSIGNED INTEGER DEFAULT 100,
    subscribers UNSIGNED INTEGER DEFAULT 100,
    thumbnail TEXT NOT NULL
)