from src.models.models import User, db
from src.utils.decorators import handle_logic_exceptions


class UserLogic:

    @handle_logic_exceptions(default_message="Error al obtener los usuarios")
    def get_users(self) -> list[User]:
        """
        Retrieves all users from the database.
        Returns:
            list: A list of dictionaries representing active users.
        Raises:
            ValueError: If no active users are found.
            SQLAlchemyError: If there is an error querying the database.
            Exception: For any other exception that occurs.
        """
        all_users = User.query.order_by(User.id).all()

        if not all_users:
            raise ValueError("No se pueden obtener los usuarios")

        serialized_users = [user.as_dict() for user in all_users]

        return serialized_users

    @handle_logic_exceptions(default_message="Error al obtener el usuario por ID")
    def get_user_by_id(self, id: int) -> User:
        """
        Retrieves a user by their ID.
        Args:
            id (int): The ID of the user to retrieve.
        Returns:
            User: The found user.
        Raises:
            ValueError: If the user is not found.
            SQLAlchemyError: If there is an error querying the database.
            Exception: For any other exception that occurs.
        """

        user = User.query.get(id)

        if not user:
            raise ValueError("Usuario no encontrado")

        return user

    @handle_logic_exceptions(default_message="Error al registrar el usuario")
    def save_user(self, user_data: dict) -> User:
        """
        Saves a new user to the database.
        Args:
            user_data (dict): The data of the user to save.
        Returns:
            User: The saved user.
        Raises:
            ValueError: If required fields are missing in user_data.
            SQLAlchemyError: If there is an error saving the user to the database.
            Exception: For any other exception that occurs.
        """

        required_data = ["username", "password", "fullname", "rol", "access_level"]

        missing = [field for field in required_data if field not in user_data]

        if missing:
            raise ValueError(f"Faltan los siguientes campos: {', '.join(missing)}")

        new_user = User(
            username=user_data["username"],
            password=user_data["password"],
            fullname=user_data["fullname"],
            rol=user_data["rol"],
            access_level=user_data["access_level"],
        )

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @handle_logic_exceptions(default_message="Error al actualizar el usuario")
    def update_user(self, id_user: int, user_data: dict) -> User:
        """
        Updates a user in the database.
        Args:
            id_user (int): The ID of the user to update.
            user_data (dict): The new data for the user.
        Returns:
            User: The updated user.
        Raises:
            ValueError: If the user is not found or required fields are missing.
            SQLAlchemyError: If there is an error updating the user in the database.
            Exception: For any other exception that occurs.
        """

        user_to_update = User.query.get(id_user)

        if not user_to_update:
            raise ValueError("Usuario no encontrado")

        for key, value in user_data.items():
            setattr(user_to_update, key, value)

        user_to_update.updated_at = db.func.now()

        db.session.commit()

        return user_to_update

    def delete_user(self, id_user: int) -> User:
        """
        Deletes a user from the database by marking them as inactive.
        Args:
            id_user (int): The ID of the user to delete.
        Returns:
            User: The deleted user.
        Raises:
            ValueError: If the user is not found.
            SQLAlchemyError: If there is an error querying the database.
            Exception: For any other exception that occurs.
        """

        user_to_delete = User.query.get(id_user)

        if not user_to_delete:
            raise ValueError("Usuario no encontrado")

        user_to_delete.active = False
        user_to_delete.updated_at = db.func.now()

        db.session.commit()

        return user_to_delete
