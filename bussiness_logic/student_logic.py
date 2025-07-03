
from datetime import datetime
from src.models.models import Student, db

from src.utils.decorators import handle_logic_exceptions


class StudentLogic:

    @handle_logic_exceptions(default_message="Error fetching active students")
    def get_studentes(self) -> list[Student]:
            """
            Fetches all active students from the database.
            Returns:
                list: A list of dictionaries representing active students.
            Raises:
                ValueError: If no active students are found.
                """

            active_students = Student.query.filter(
                Student.active == True
            ).order_by(
                Student.id
            )

            if not active_students:
                raise ValueError(f'No active students found in the database')
            
            serialized_active_students = [student.as_dict() for student in active_students]

            return serialized_active_students
    

    @handle_logic_exceptions(default_message="Error fetching all students")
    def get_all_students(self) -> list[Student]:
         """
        Fetches all students from the database, both active and inactive.
        Returns:
            list: A list of dictionaries representing all students.
        Raises:
            ValueError: If no students are found.
         """
         
         all_students = Student.query.order_by(Student.id)

         if not all_students:
                raise ValueError(f'No students found in the database')
         
         serialized_all_students = [student.as_dict() for student in all_students]

         return serialized_all_students
    

    @handle_logic_exceptions(default_message="Error fetching student by ID")
    def get_student_by_id(self, id: int) -> Student:
        """
        Fetches a student by their ID from the database.
        Args:
            id (int): The ID of the student to fetch.
        Returns:
            Student: The student object if found.
        Raises:
            ValueError: If the student with the given ID is not found.
        """
          
        founded_student = db.session.get(Student, id)

        if not founded_student:
            raise ValueError(f'Student with ID {id} not found')
        
        return founded_student
    

    @handle_logic_exceptions(default_message="Error deleting student")
    def delete_student(self, id: int) -> Student:
        """
        'Deletes' a student by setting their active status to False.
        Args:
            id (int): The ID of the student to delete.
        Returns:
            Student: The updated student object if found and marked as inactive.
        Raises:
            ValueError: If the student with the given ID is not found.
        """
         
        founded_student = db.session.get(Student, id)

        if not founded_student:
            raise ValueError(f'Student with ID {id} not found')
        
        founded_student.active = False
        db.session.commit()

        return founded_student
    

    @handle_logic_exceptions(default_message="Error saving student")
    def save_student(self, student_data: dict[str, any]) -> Student:
        """
        Saves a new student to the database.
        Args:
            student_data (dict): A dictionary containing student data.
        Returns:
            Student: The newly created student object.
        Raises:
            ValueError: If required fields are missing in the student data.
        """
        required_data = ["dni", "name", "surnames", "address", "email", "active"]

        missing = [field for field in required_data if field not in student_data]

        if missing:
             raise ValueError(f'Missing required fields for creation: {", ".join(missing)}')
        
        new_student = Student(
            dni=student_data["dni"],
            names=student_data["names"],
            surnames=student_data["surnames"],
            address=student_data["address"],
            email=student_data["email"],
            active=student_data["active"]
        )

        db.session.add(new_student)
        db.session.commit()

        return new_student
    

    @handle_logic_exceptions(default_message="Error updating student")
    def update_student(self, id: int, student_data: dict[str, any]) -> Student:
        """
        Updates an existing student in the database.
        Args:
            id (int): The ID of the student to update.
            student_data (dict): A dictionary containing updated student data.
        Returns:
            Student: The updated student object.
        Raises:
            ValueError: If the student with the given ID is not found or if no data is provided for update.
        """
        
        founded_student = db.session.get(Student, id)

        if not founded_student:
            raise ValueError(f'Student with ID {id} not found')
        
        if not student_data:
            raise ValueError('No data provided for update')

        for key, value in student_data.items():
            setattr(founded_student, key, value)

        founded_student.updated_at = datetime.now()

        db.session.commit()

        return founded_student
    

    @handle_logic_exceptions(default_message="Error associating student with tutor")
    def associate_tutor_with_student(self, student_id: int, tutor_id: int) -> dict[str, any]:
        """
        Associates a tutor with a student by their IDs.
        Args:
            student_id (int): The ID of the student to associate with the tutor.
            tutor_id (int): The ID of the tutor to associate with the student.
        Returns:
            dict: A dictionary containing a success message.
        Raises:
            ValueError: If the student or tutor with the given IDs is not found, or if the tutor is already associated with the student.
            
        """
         
        
        student = db.session.get(Student, student_id)

        if not student:
            raise ValueError(f'Student with ID {student_id} not found')
        
        tutor = db.session.get(Student, tutor_id)

        if not tutor:
            raise ValueError(f'Tutor with ID {tutor_id} not found')
        
        if tutor_id in student.tutors:
            raise ValueError(f'Tutor with ID {tutor_id} is already associated with student {student_id}')
        
        student.tutors.append(tutor)
        db.session.commit()

        return {"message": "Relacion entre alumno y tutor establecida con éxito"}

         
  


