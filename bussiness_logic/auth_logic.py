from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from src.models.models import User, db
from src.utils.security import generate_token

class AuthLogic:

    def login_user(self, login_data: dict[str, Any]) -> dict[str, Any]:

        try:
            founded_user = User.query.filter(User.username == login_data.get('username')).first()

            if not founded_user:
                raise ValueError(f"User with the username {login_data.get('username')} not found in the database.")

            if founded_user.password != login_data.get('password'):
                raise ValueError("Incorrect password provided.")
            
            token = generate_token(founded_user.id)

            return({'message': 'Usuario autenticado.',
                    'username': founded_user.username,
                    'user_id': founded_user.id,
                    'access_level': founded_user.access_level,
                    'token': token})
        
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")

        except Exception as e:
            #Capturar cualquier otra excepcion inesperada
            raise Exception(f"An unexpected error ocurred while fetching attendances: {e}") from e


    def register_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        
        try:
            new_user = User(username=user_data.get('username'), 
                            password=user_data.get('password'), 
                            fullname=user_data.get('fullname'), 
                            rol=user_data.get('rol'),
                            access_level=user_data.get('access_level'))
            db.session.add(new_user)
            db.session.commit()

            return {'message': 'User registered successfully.'}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"An unexpected error ocurred while registering user: {e}") from e