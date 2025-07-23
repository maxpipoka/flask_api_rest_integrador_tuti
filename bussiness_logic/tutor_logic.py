


from datetime import datetime
from typing import List
from src.models.models import Tutor, db

from src.utils.decorators import handle_logic_exceptions


class TutorLogic:

    @handle_logic_exceptions(default_message="Error al obtener los tutores activos")
    def get_tutors(self) -> List[Tutor]:
        """
        Obtiene todos los tutores activos de la base de datos.
        Returns:
            List[Tutor]: Una lista de diccionarios que representan los tutores activos. 
        Raises:
            ValueError: Si no se encuentran tutores activos.
            SQLAlchemyError: Si hay un error al consultar la base de datos.
            Exception: Para cualquier otra excepción que ocurra.

        """

        all_tutors = Tutor.query.filter(Tutor.active == True).order_by(
            Tutor.id).all()
        
        if not all_tutors:
            raise ValueError("No se pueden obtener los tutores activos")
        
        seriealized_active_tutors = [tutor.as_dict() for tutor in all_tutors]

        return seriealized_active_tutors

    
    @handle_logic_exceptions(default_message="Error al obtener el tutor por ID")
    def get_tutor_by_id(self, id: int) -> dict[str, any]:
        """
        Obtiene un tutor por su ID.
        Args:
            id (int): El ID del tutor a obtener.
        Returns:
            dict: Un diccionario que representa el tutor encontrado.
        Raises:
            ValueError: Si no se encuentra el tutor con el ID proporcionado.
            SQLAlchemyError: Si hay un error al consultar la base de datos.
            Exception: Para cualquier otra excepción que ocurra.
        """
        
        founded_tutor = db.session.get(Tutor, id)

        if not founded_tutor:
            raise ValueError(f"No se encuentra el tutor con el ID {id}")
        
        return founded_tutor


    @handle_logic_exceptions(default_message="Error al eliminar el tutor")
    def delete_tutor(self, id: int) -> Tutor:
        """
        Elimina un tutor por su ID.
        Args:
            id (int): El ID del tutor a eliminar.
        Returns:
            Tutor: El tutor eliminado.
        Raises:
            ValueError: Si no se encuentra el tutor con el ID proporcionado.
            SQLAlchemyError: Si hay un error al consultar la base de datos.
            Exception: Para cualquier otra excepción que ocurra.
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
        Guarda un nuevo tutor en la base de datos.
        Args:
            tutor_data (dict): Un diccionario que contiene los datos del tutor a guardar.
        Returns:
            Tutor: El tutor guardado.
        Raises:
            ValueError: Si hay un error al guardar el tutor.
            SQLAlchemyError: Si hay un error al consultar la base de datos.
            Exception: Para cualquier otra excepción que ocurra.
        """
        
        required_data = ["dni", "names", "surnames", "address", "email", "active"]

        missing = [field for field in required_data if field not in tutor_data]

        if missing:
            raise ValueError(f"Faltan campos requeridos para la creación: {', '.join(missing)}")
        
        new_tutor = Tutor(
            dni=tutor_data["dni"],
            names=tutor_data["names"],
            surnames=tutor_data["surnames"],
            address=tutor_data["address"],
            email=tutor_data["email"],
            active=tutor_data.get("active")
        )

        db.session.add(new_tutor)
        db.session.commit()

        return new_tutor


    
    def update_tutor(self, id_tutor: int, tutor_data: dict[str, any]) -> Tutor:
        """
        Actualiza un tutor existente en la base de datos.
        Args:
            id_tutor (int): El ID del tutor a actualizar.
            tutor_data (dict): Un diccionario que contiene los datos del tutor a actualizar.
        Returns:
            Tutor: El tutor actualizado.
        Raises:
            ValueError: Si no se encuentra el tutor con el ID proporcionado o si hay un error al actualizar.
            SQLAlchemyError: Si hay un error al consultar la base de datos.
            Exception: Para cualquier otra excepción que ocurra.
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



