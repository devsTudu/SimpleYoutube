import sqlite3
from datetime import datetime, date
import random


def execute_query(db_path: str, query: str, params: tuple = ()) -> None:
    """Helper function to execute an SQL query."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        print(f"Query executed successfully: {query[:50]}...")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


# Example Usage:

DB_PATH = "local.db"  # Path to your SQLite database file


def add_course(id, name, desc, smallimg, bigimg, creatorid, datepub):
    # --- Inserting a Course ---
    course_data = (
        id,
        name,
        desc,
        smallimg,
        bigimg,
        creatorid,
        datepub,
        datetime.now().isoformat(),
    )
    execute_query(
        DB_PATH,
        """
    INSERT INTO courses (
        course_id, course_name, course_description, thumbnail_small,
        thumbnail_big, creator_id, published_date, last_updated_date
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """,
        course_data,
    )
def add_lesson_basic(lesson_id, video_id, lesson_title, thumbnail_small, thumbnail_big):
    data = (
        lesson_id,
        video_id,
        lesson_title,
        thumbnail_small,
        thumbnail_big,
        datetime.now().isoformat(),
    )
    execute_query(
        DB_PATH,
        """
        INSERT OR REPLACE INTO lessons (
            lesson_id, video_id, lesson_title, thumbnail_small, thumbnail_big, last_updated_date
        ) VALUES (?, ?, ?, ?, ?, ? );
        """,
        params=data
    )
def add_lesson_all(
            lesson_id, video_id, lesson_title, lesson_description, creator_id,
            published_date, thumbnail_small, thumbnail_big, duration_minutes,
            views_count, likes_count, comments_count,):
    query = """INSERT OR REPLACE INTO lessons (
            lesson_id, video_id, lesson_title, lesson_description, creator_id,
            published_date, thumbnail_small, thumbnail_big, duration_minutes,
            views_count, likes_count, comments_count, last_updated_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    data = (
            lesson_id, video_id, lesson_title, lesson_description, creator_id,
            published_date, thumbnail_small, thumbnail_big, duration_minutes,
            views_count, likes_count, comments_count,datetime.now().isoformat())
    execute_query(DB_PATH,query,data)    
def add_creators(creator_id, creator_name, title, description, thumbnail_small,
    thumbnail_big, views_count, subscriber_count, lesson_count):
    data = (creator_id, creator_name, title, description, thumbnail_small,
    thumbnail_big, views_count, subscriber_count, lesson_count,datetime.now().isoformat() )
    query = """INSERT OR REPLACE INTO creators (
    creator_id, creator_name, title, description, thumbnail_small,
    thumbnail_big, views_count, subscriber_count, lesson_count, last_updated_date
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    execute_query(DB_PATH,query,data)
def add_course_lesson(course_id,lesson_id):
    data = (course_id,lesson_id)
    query = """INSERT OR IGNORE INTO course_lessons (course_id, lesson_id)
            VALUES (?, ?)"""
    execute_query(DB_PATH,query,data)
def add_notes(user_id, course_id, lesson_id, note_content):
    data = (
            user_id,
            course_id,
            lesson_id,
            note_content,
            datetime.now().isoformat())
    query = """INSERT INTO notes (
            user_id, course_id, lesson_id, note_content, created_at
        ) VALUES (?, ?, ?, ?, ?);"""
    execute_query(DB_PATH,query,data)

def log_watch_event(user_id,lesson_id,course_id):
    # --- Logging a Lesson Watch Event ---
    event_timestamp = datetime.now().isoformat()
    execute_query(
        DB_PATH,
        """
    INSERT INTO user_activity (
        user_id, event_type, course_id, lesson_id, timestamp
    ) VALUES (?, ?, ?, ?, ?);
    """,
        (user_id, "LESSON_WATCHED", course_id, lesson_id, event_timestamp),
    )

def updating_note(updated_note,note_id,user_id):
    # --- Updating a Note ---
    
    execute_query(
        DB_PATH,
        """
    UPDATE notes
    SET
        note_content = ?,
        created_at = ?
    WHERE note_id = ? AND user_id = ?;
    """,
        (updated_note, datetime.now().isoformat(), note_id, user_id),
    )

def deleting_note(note_id, user_id):
    # --- Deleting a Note ---
    execute_query(DB_PATH,
                  "DELETE FROM notes WHERE note_id = ? AND user_id = ?;",
                  (note_id, user_id))


user_id = "debasish"

# Creating Creators
for i_s in range(random.randint(5,8)):
    i = str(i_s)
    add_creators("cid"+i,"cname"+i,"ctitle"+i,'cdesc'+i,'csmall'+i,'cbig'+i,i_s,i_s,i_s)
    
    for j in range(random.randint(5,8)):
        j = str(j)
        # Create a course for each creator
        course_id = "course" + j + "by " + "cid"+i
        add_course(
            course_id,
            "Course Name " + j,
            "Course Description " + i,
            "course_small_" + i,
            "course_big_" + i,
            "cid" + i,
            date.today().isoformat(),
        )

        # Create random number of lessons for each course
        num_lessons = random.randint(2, 5)
        lesson_ids = []
        for j in range(num_lessons):
            lesson_id = f"lesson_{i}_{j}"
            video_id = f"vid_{i}_{j}"
            lesson_title = f"Lesson Title {i}-{j}"
            lesson_description = f"Lesson Description {i}-{j}"
            thumbnail_small = f"lesson_small_{i}_{j}"
            thumbnail_big = f"lesson_big_{i}_{j}"
            duration_minutes = random.randint(5, 60)
            views_count = random.randint(0, 1000)
            likes_count = random.randint(0, 500)
            comments_count = random.randint(0, 100)
            creator_id = "cid" + i
            published_date = date.today().isoformat()

            add_lesson_all(
                lesson_id, video_id, lesson_title, lesson_description, creator_id,
                published_date, thumbnail_small, thumbnail_big, duration_minutes,
                views_count, likes_count, comments_count
            )
            add_course_lesson(course_id, lesson_id)
            lesson_ids.append(lesson_id)

            # Add a note for some lessons
            if random.choice([True, False]):
                note_content = f"Note for {lesson_title}"
                add_notes(user_id, course_id, lesson_id, note_content)


