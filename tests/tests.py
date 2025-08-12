from src.youtube_api import (
    get_creator_details_by_id,
    get_lesson_details_by_id,
    get_lessons_for_course,
    search_courses
)


from src.routes.client import client

def test_playlists():
    q_id = "PLTWGH5orWwL1-W-t21jQOIWUO6GKsc0ir"
    raw = get_lessons_for_course(client, q_id)
    assert raw is not None
    assert len(raw.lessons) > 0


def test_video_id():
    q_id = "gfhtaP5Wq7M"
    video_detail = get_lesson_details_by_id(client, q_id)
    print(video_detail)
    assert video_detail is not None
    assert video_detail.lesson_title == "#39 Python Tutorial for Beginners | Factorial"


def test_query():
    query = "Python Learning"
    resp = search_courses(client,query)
    print(resp)
    assert len(resp)>10


def test_channel():
    query = "UCJhvzsRo8W-pSHpjpXfEPSw"
    resp = get_creator_details_by_id(client,query)
    print(resp)
    assert resp
    
