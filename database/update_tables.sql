-- Insert Courses
INSERT OR REPLACE INTO
    courses (
        course_id,
        course_name,
        course_description,
        thumbnail_small,
        thumbnail_big,
        creator_id,
        published_date,
        last_updated_date
    )
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- Insert lessons
INSERT OR REPLACE INTO
    lessons (
        lesson_id,
        video_id,
        lesson_title,
        lesson_description,
        creator_id,
        published_date,
        thumbnail_small,
        thumbnail_big,
        duration_minutes,
        views_count,
        likes_count,
        comments_count,
        last_updated_date
    )
VALUES (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    );

-- Insert Creators
INSERT OR REPLACE INTO
    creators (
        creator_id,
        creator_name,
        title,
        description,
        thumbnail_small,
        thumbnail_big,
        views_count,
        subscriber_count,
        lesson_count,
        last_updated_date
    )
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

-- Add relations of Lesson and Course
INSERT OR IGNORE INTO
    course_lessons (course_id, lesson_id)
VALUES (?, ?);

-- Add activity
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id,
        timestamp
    )
VALUES (?, ?, ?, ?, ?);

-- Bookmark a course
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id
    )
VALUES (
        'debasish',
        'BOOKMARK',
        'course5by cid2',
        NULL
    );

-- Activity - Note Deleted
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id,
        timestamp
    )
VALUES (?, 'NOTE_DELETED', ?, ?, ?);

-- Activity a note taken
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id,
        timestamp
    )
VALUES (?, 'NOTE_TAKEN', ?, ?, ?);

-- Activity lesson watched
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id,
        timestamp
    )
VALUES (
        'debasish',
        'LESSON_WATCHED',
        'course5by cid2',
        'lesson_2_0',
        '2025-08-13 12:53:17'
    );

-- Activity Course Enrollment
INSERT INTO
    user_activity (
        user_id,
        event_type,
        course_id,
        lesson_id
    )
VALUES (
        'debasish',
        'ENROLL',
        'course5by cid2',
        NULL
    );

-- Insert a new note
INSERT INTO
    notes (
        user_id,
        course_id,
        lesson_id,
        note_content,
        created_at
    )
VALUES (?, ?, ?, ?, ?);

-- Update an existing note
UPDATE notes
SET
    note_content = ?,
    created_at = ? -- You might update 'created_at' to 'updated_at' for edits
WHERE
    note_id = ?
    AND user_id = ?;

-- Delete a note
DELETE FROM notes WHERE note_id = ? AND user_id = ?;