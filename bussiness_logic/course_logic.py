from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from src.models.models import Course, Student, db

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
        Deletes a course by its ID, marking it as inactive.
        Args:
            id (int): The ID of the course to be deleted.
        Returns:
            Course: The updated course object with active set to False.
        Raises:
            ValueError: If the course does not exist or there is an error retrieving it.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        
        """
        
        try:
            founded_course = db.session.get(Course)

            founded_course.active = False
            founded_course.updated_at = datetime.now()
            db.session.commit()

            return founded_course
        
        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Error retrieving course: {str(e)}")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error retrieving course: {str(e)}")


    def asociate_student_to_course(self, course_id: int, student_id: int) -> dict[str]:
        """
        Associates a student with a course.
        Args:
            course_id (int): The ID of the course.
            student_id (int): The ID of the student.
        Returns:
            None
        Raises:
            ValueError: If the course or student does not exist or there is an error retrieving them.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        """
        
        try:
            founded_student = db.session.get(Student, student_id)
            founded_course = db.session.get(Course, course_id)

            if not founded_student or not founded_course:
                raise ValueError("Course or Student does not exist")

            founded_course.students.append(founded_student)
            db.session.commit()
            return {"message": "Student associated to course successfully"}

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Error associating student to course: {str(e)}")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error associating student to course: {str(e)}")
        

    def save_course(self, course_data: dict) -> Course:
        """
        Saves a new course to the database.
        Args:
            course_data (dict): A dictionary containing course data.
        Returns:
            Course: The newly created course object.
        Raises:
            ValueError: If the course data is invalid or there is an error saving it.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        """

        try:
            if not course_data:
                raise ValueError("Course data is missing or invalid")

            new_course = Course(
                level=course_data.get('level'),
                year=course_data.get('year'),
                division=course_data.get('division'),
                associated_user=course_data.get('associated_user'),
                active=True,
                current=True
            )

            db.session.add(new_course)
            db.session.commit()

            return new_course
        
        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Error saving course: {str(e)}")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error saving course: {str(e)}")

    def update_course(self, course_data: dict[str, str], id_course: int) -> Course:
        """
        Updates an existing course in the database.
        Args:
            course_data (dict): A dictionary containing the updated course data.
            id_course (int): The ID of the course to be updated.
        Returns:
            Course: The updated course object.
        Raises:
            ValueError: If the course data is invalid or there is an error updating it.
            SQLAlchemyError: If there is a database error.
            Exception: For any other exceptions that occur.
        
        """

        try:
            founded_course = db.session.get(Course, id_course)

            if not founded_course:
                raise ValueError("Course does not exist")
            
            if not course_data:
                raise ValueError("No data provided for update")
            
            for key, value in course_data.items():
                if key not in ['level', 'division', 'year', 'associated_user']:
                    raise ValueError(f"Invalid field for update: {key}")
                setattr(founded_course, key, value)
            
            founded_course.updated_at = datetime.now()
            
            db.session.commit()

            return founded_course
        
        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Error updating course: {str(e)}")
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise SQLAlchemyError(f"Database error: {str(e)}")
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating course: {str(e)}")

