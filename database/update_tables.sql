-- Active: 1739596619152@@127.0.0.1@3306
-- Videos Table
INSERT or REPLACE INTO "videoinfo"("thumbnail_url","video_id","videoTitle","videoDescr","channel_id") 
VALUES('hello_world','kill','simple','Simpleton','hero2');

-- Mark video started
UPDATE "videoInfo" SET "startedOn" = CURRENT_TIMESTAMP WHERE video_id="kill";

-- Mark Video Completed
UPDATE "videoInfo" SET "completedOn" = CURRENT_TIMESTAMP WHERE video_id="sDFG";


-- Notes table
INSERT INTO "Notes"("video_id","notes_content") VALUES('sega','hello how are you');

-- Update Notes
UPDATE "Notes" SET "lastUpdated"= CURRENT_TIMESTAMP, notes_content= "I am good"
WHERE note_id=1;

--- Activity Table
INSERT INTO "Activity"("searchTerm","course_id","lesson_id","coursename","lessonname","course_started","course_completed","lesson_completed","note_id","note_created","note_edited","note_deleted") 
VALUES('searched','courseid','lessonid','coursename','lesson_name',true,true,false,'idofnote',true,false,true);

-- Playlist
INSERT INTO "Playlists"("playlistid","total_videos","channel_id") VALUES('pl1',4,'ch1');

INSERT INTO Playlist_Video_Junction (playlist_id, video_id)
VALUES (5, 101);

-- Channel
INSERT INTO channel(channel_id, name, subscribers, views, thumbnail)
VALUES("Heelo","Khan",123,234,"thumpsup")
