
from sqlalchemy.exc import SQLAlchemyError

from src.models.models import Course, db

class CourseLogic:

    def get_courses(self) -> list[Course]:
        """
        Retrieves all courses from the database, ordered by level, year, and division.
        Returns:
            list[Course]: A list of serialized course dictionaries.
        Raises:
            ValueError: If there is an error retrieving courses.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        """

        try:
            all_courses = Course.query.order_by(Course.level, Course.year, Course.division)

            if not all_courses:
                raise ValueError("No courses found")

            serialized_courses = [course.as_dict() for course in all_courses]
            
            return serialized_courses
        
        except ValueError as e:
            raise ValueError(f"Error retrieving courses: {str(e)}")
        
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Error retrieving courses: {str(e)}")
        

    def get_courses_by_preceptor(self):
        pass

    def get_course_by_id(self):
        pass

    def delete_course(self):
        pass

    def asociate_student_to_course(self):
        pass

    def save_course(self):
        pass

    def update_course(self):
        pass

