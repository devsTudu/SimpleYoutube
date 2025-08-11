-- Active: 1739596619152@@127.0.0.1@3306

-- Activity Table
SELECT * from "Activity" ORDER BY id DESC;

-- Select videos from video_Id
SELECT * from "videoinfo" 
WHERE video_id="kill";

SELECT * from "videoinfo";

-- Select notes from video_id
SELECT * FROM "Notes" 
WHERE video_id = "sega";

SELECT * from "Notes";

SELECT * FROM "Playlists"
WHERE pl_id="1234";

-- Playlist
SELECT *
FROM "videoInfo" AS V
JOIN Playlist_Video_Junction AS PVJ ON V.video_id = PVJ.video_id
WHERE PVJ.playlist_id = "pl1";

SELECT *
FROM Playlists AS P
JOIN Playlist_Video_Junction AS PVJ ON P.playlistid = PVJ.playlist_id
WHERE PVJ.video_id = "kill";


SELECT * from channel
WHERE channel_id="Heelo"
;