CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    course_description TEXT,
    thumbnail_small TEXT,
    thumbnail_big TEXT NOT NULL,
    creator_id TEXT,
    published_date TEXT,
    last_updated_date TEXT NOT NULL
);

CREATE TABLE lessons (
    lesson_id TEXT PRIMARY KEY,
    video_id TEXT NOT NULL,
    lesson_title TEXT NOT NULL,
    lesson_description TEXT,
    creator_id TEXT,
    published_date TEXT,
    thumbnail_small TEXT,
    thumbnail_big TEXT NOT NULL,
    duration_minutes INTEGER,
    views_count INTEGER,
    likes_count INTEGER,
    comments_count INTEGER,
    last_updated_date TEXT NOT NULL
);

CREATE TABLE creators (
    creator_id TEXT PRIMARY KEY,
    creator_name TEXT NOT NULL,
    title TEXT,
    description TEXT,
    thumbnail_small TEXT,
    thumbnail_big TEXT NOT NULL,
    views_count INTEGER,
    subscriber_count INTEGER,
    lesson_count INTEGER,
    last_updated_date TEXT NOT NULL
);

CREATE TABLE course_lessons (
    course_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    PRIMARY KEY (course_id, lesson_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
);

CREATE TABLE user_activity (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- e.g., 'ENROLL', 'BOOKMARK', 'LESSON_WATCHED', 'NOTE_TAKEN'
    course_id TEXT,
    lesson_id TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
);

CREATE TABLE notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    note_content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id)
);