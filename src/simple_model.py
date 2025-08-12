from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date # Using date for simplicity, can use datetime for timestamps

## --- Core Models for API Response Data ---

# Reusable model for basic creator information often embedded in other responses
class CreatorInfo(BaseModel):
    creator_id: str
    creator_name: str

# Model for individual courses returned by 'Get relevant courses'
class Course(BaseModel):
    course_id: str
    course_name: str
    course_description: Optional[str] = None
    thumbnail_small: Optional[str] = None
    thumbnail_big: str
    creator_name: str # Embedded creator name
    creator_id: str   # Embedded creator ID
    published_date: Optional[date] = None # Assuming date format like 'YYYY-MM-DD'

# Model for individual lessons as part of a course detail response
class LessonInCourseDetail(BaseModel):
    lesson_id: str
    lesson_title: str
    lesson_description: Optional[str] = None
    creator_name: str
    creator_id: str
    published_date: Optional[date] = None
    thumbnail_small: Optional[str] = None
    thumbnail_big: str

# Model for the response from 'Get Course Detail'
# This endpoint returns a course's details along with its associated lessons.
class CourseDetailResponse(BaseModel):
    # Assuming the API provides course-level details here too,
    lessons: List[LessonInCourseDetail] = Field(...,
                                                description="List of lessons associated with the course.")

# Model for the response from 'Get creator detail'
class CreatorDetail(BaseModel):
    creator_id: str # Including ID for clarity, assuming it's part of the response for the queried creator
    creator_name: str # Including name for clarity
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_small: Optional[str] = None
    thumbnail_big: str
    views_count: int = Field(0) # Use Field for alias if API uses camelCase
    subscriber_count: int = Field(0)
    lesson_count: int = Field(0)

# Model for the response from 'Get lesson detail'
class LessonDetail(BaseModel):
    lesson_id: str
    video_id: str
    creator_id: str
    creator_name: str
    lesson_title: str
    lesson_description: Optional[str] = None
    publish_date: Optional[date] = None
    thumbnail_small: Optional[str] = None
    thumbnail_big: str
    category_id: Optional[str] = Field(None)
    duration_minutes: int = 1
    views_count: int = Field(0)
    like_count: int = Field(0)
    comment_count: int = Field(0)

