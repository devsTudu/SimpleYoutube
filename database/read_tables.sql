
-- ---------- --- New Table Operations

-- Get the streak data
SELECT
  COUNT(*) AS streak
FROM (
  SELECT
    strftime('%Y-%m-%d', timestamp) AS activity_date,
    strftime('%Y-%m-%d', timestamp, '-' || ROW_NUMBER() OVER (ORDER BY strftime('%Y-%m-%d', timestamp) DESC) || ' days') AS streak_group
  FROM (
    SELECT DISTINCT
      timestamp
    FROM user_activity
    WHERE user_id = 'debasish' AND event_type = 'LESSON_WATCHED'
  )
)
GROUP BY
  streak_group
ORDER BY
  activity_date DESC
LIMIT 1;


-- Enrolled Courses
SELECT
    C.thumbnail_big,
    C.course_name AS course_title,
    C.course_id,
    CR.creator_name,
    CAST(COUNT(DISTINCT UL.lesson_id) AS REAL) / (SELECT COUNT(*) FROM course_lessons WHERE course_id = C.course_id) AS progress_percentage
FROM courses AS C
JOIN creators AS CR ON C.creator_id = CR.creator_id
JOIN user_activity AS UA ON C.course_id = UA.course_id
LEFT JOIN (
    SELECT DISTINCT lesson_id, course_id
    FROM user_activity
    WHERE user_id = 'debasish' AND event_type = 'LESSON_WATCHED'
) AS UL ON UA.course_id = UL.course_id
WHERE UA.user_id = 'debasish' AND UA.event_type = 'ENROLL'
GROUP BY C.course_id;

-- Bookmarked Courses
SELECT
    C.course_name AS course_title,
    C.course_id,
    C.thumbnail_big,
    CR.creator_name,
    CR.creator_id
FROM courses AS C
JOIN creators AS CR ON C.creator_id = CR.creator_id
JOIN user_activity AS UA ON C.course_id = UA.course_id
WHERE UA.user_id = 'debasish' AND UA.event_type = 'BOOKMARK';

-- Course Page -added check for watched lesson
SELECT
    CR.creator_name,
    CR.creator_id,
    CR.thumbnail_small AS creator_image,
    L.video_id,
    L.lesson_title,
    L.lesson_description,
    L.thumbnail_small,
    L.duration_minutes, 
    CASE
        WHEN UA.lesson_id IS NOT NULL THEN 1
        ELSE 0
    END AS is_watched
FROM lessons AS L
JOIN course_lessons AS CL ON L.lesson_id = CL.lesson_id
JOIN courses AS C ON CL.course_id = C.course_id
JOIN creators AS CR ON L.creator_id = CR.creator_id
LEFT JOIN user_activity AS UA ON
    L.lesson_id = UA.lesson_id AND
    UA.user_id = 'debasish' AND -- Parameter for user_id
    UA.event_type = 'LESSON_WATCHED'
WHERE C.course_id = 'course5by cid2'; -- Parameter for course_id


-- Get all the Notes
SELECT *
FROM notes
WHERE user_id = 'debasish';

-- Get notes for the lesson
SELECT
    note_content,
    created_at
FROM notes
WHERE user_id = ? AND lesson_id = ?;

-- Get Notes for courses
SELECT
    N.note_content,
    N.created_at,
    L.lesson_title
FROM notes AS N
JOIN lessons AS L ON N.lesson_id = L.lesson_id
WHERE N.user_id = ? AND N.course_id = ?;