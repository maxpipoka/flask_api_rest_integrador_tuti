from datetime import datetime
from typing import List
from src.models.models import Tutor, db

from src.utils.decorators import handle_logic_exceptions


class TutorLogic:

    @handle_logic_exceptions(default_message="Error al obtener los tutores activos")
    def get_tutors(self) -> List[Tutor]:
        """
        Retrieves all active tutors from the database.
        Returns:
            List[Tutor]: A list of dictionaries representing the active tutors.
        Raises:
            ValueError: If no active tutors are found.
            SQLAlchemyError: If there is a database query error.
            Exception: For any other exception that occurs.

        """

        all_tutors = Tutor.query.filter(Tutor.active == True).order_by(Tutor.id).all()

        if not all_tutors:
            raise ValueError("No se pueden obtener los tutores activos")

        seriealized_active_tutors = [tutor.as_dict() for tutor in all_tutors]

        return seriealized_active_tutors

    @handle_logic_exceptions(default_message="Error al obtener el tutor por ID")
    def get_tutor_by_id(self, id: int) -> dict[str, any]:
        """
        Retrieves a tutor by their ID.
        Args:
            id (int): The ID of the tutor to retrieve.
        Returns:
            dict: A dictionary representing the found tutor.
        Raises:
            ValueError: If no tutor is found with the provided ID.
            SQLAlchemyError: If there is a database query error.
            Exception: For any other exception that occurs.
        """

        founded_tutor = db.session.get(Tutor, id)

        if not founded_tutor:
            raise ValueError(f"No se encuentra el tutor con el ID {id}")

        return founded_tutor

    @handle_logic_exceptions(default_message="Error al eliminar el tutor")
    def delete_tutor(self, id: int) -> Tutor:
        """
        Deletes a tutor by their ID.
        Args:
            id (int): The ID of the tutor to delete.
        Returns:
            Tutor: The deleted tutor.
        Raises:
            ValueError: If no tutor is found with the provided ID.
            SQLAlchemyError: If there is a database query error.
            Exception: For any other exception that occurs.
        """

        tutor_to_delete = db.session.get(Tutor, id)

        if not tutor_to_delete:
            raise ValueError(f"No se encuentra el tutor con el ID {id}")

        tutor_to_delete.active = False

        db.session.commit()

        return tutor_to_delete

    @handle_logic_exceptions(default_message="Error al guardar el tutor")
    def save_tutor(self, tutor_data: dict[str, any]) -> Tutor:
        """
        Saves a new tutor to the database.
        Args:
            tutor_data (dict): A dictionary containing the tutor data to save.
        Returns:
            Tutor: The saved tutor.
        Raises:
            ValueError: If there is an error saving the tutor.
            SQLAlchemyError: If there is a database query error.
            Exception: For any other exception that occurs.
        """

        required_data = ["dni", "names", "surnames", "address", "email", "active"]

        missing = [field for field in required_data if field not in tutor_data]

        if missing:
            raise ValueError(
                f"Faltan campos requeridos para la creación: {', '.join(missing)}"
            )

        new_tutor = Tutor(
            dni=tutor_data["dni"],
            names=tutor_data["names"],
            surnames=tutor_data["surnames"],
            address=tutor_data["address"],
            email=tutor_data["email"],
            active=tutor_data.get("active"),
        )

        db.session.add(new_tutor)
        db.session.commit()

        return new_tutor

    @handle_logic_exceptions(default_message="Error al actualizar el tutor")
    def update_tutor(self, id_tutor: int, tutor_data: dict[str, any]) -> Tutor:
        """
        Updates an existing tutor in the database.
        Args:
            id_tutor (int): The ID of the tutor to update.
            tutor_data (dict): A dictionary containing the tutor data to update.
        Returns:
            Tutor: The updated tutor.
        Raises:
            ValueError: If no tutor is found with the provided ID or if there is an update error.
            SQLAlchemyError: If there is a database query error.
            Exception: For any other exception that occurs.
        """

        tutor_to_update = db.session.get(Tutor, id_tutor)

        if not tutor_to_update:
            raise ValueError(f"No se encuentra el tutor con el ID {id_tutor}")

        if not tutor_data:
            raise ValueError("No hay datos para actualizar el tutor")

        for key, value in tutor_data.items():
            setattr(tutor_to_update, key, value)

        tutor_to_update.updated_at = datetime.now()

        db.session.commit()

        return tutor_to_update
