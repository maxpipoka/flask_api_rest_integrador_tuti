
from datetime import datetime
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
        

    def get_courses_by_preceptor(self, preceptor_id: int) -> list[Course]:
        """
        Retrieves all courses associated with a specific preceptor.
        Args:
            preceptor_id (int): The ID of the preceptor.
        Returns:
            list[Course]: A list of serialized course dictionaries associated with the preceptor.
        Raises:
            ValueError: If there is an error retrieving courses.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        """

        try:
            founded_courses = Course.query.filter(
                Course.associated_user == preceptor_id,
                Course.active == True,
                Course.current == True
            ).order_by(Course.level, Course.year, Course.division)

            if not founded_courses:
                raise ValueError("No courses found for the specified preceptor")
            
            serialized_courses = [course.as_dict() for course in founded_courses]

            return serialized_courses

        except ValueError as e:
            raise ValueError(f"Error retrieving courses: {str(e)}")
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving courses: {str(e)}")
        


    def get_course_by_id(self, id_course: int ) -> Course:
        """
        Retrieves a course by its ID.
        Args:
            id_course (int): The ID of the course.
        Returns:
            Course: A serialized course dictionary.
        Raises:
            ValueError: If the course does not exist or there is an error retrieving it.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        """

        try:
            founded_course = db.sesison.get(Course, id_course)

            if not founded_course:
                raise ValueError("Course does not exist")
            
            serialized_course = founded_course.as_dict()

            return serialized_course
        
        except ValueError as e:
            raise ValueError(f"Error retrieving course: {str(e)}")
        
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Error retrieving course: {str(e)}")

    def delete_course(self, id: int) -> Course:
        """

        
        """
        
        try:
            founded_course = db.session.get(Course)

            founded_course.active = False
            founded_course.updated_at = datetime.now()
            db.session.commit()

            return founded_course
        
        except ValueError as e:
            raise ValueError(f"Error retrieving course: {str(e)}")
        
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Error retrieving course: {str(e)}")


    def asociate_student_to_course(self):
        pass

    def save_course(self):
        pass

    def update_course(self):
        pass

