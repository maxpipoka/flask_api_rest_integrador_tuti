from functools import wraps
from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from src.utils.security import decode_token


def token_required(f):
    """
    Decorator to ensure that a valid token is provided in the request headers.

    This decorator checks for the presence of an "Authorization" header in the request.
    If the token is missing or invalid, it returns a 401 Unauthorized response.
    If the token is valid, it allows the request to proceed to the decorated function.
    Args:
        f (function): The function to be decorated.
    Returns:
        function: The decorated function that checks for a valid token.
    Raises:
        Unauthorized: If the token is missing or invalid.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            decode_token(token)
        except:
            return jsonify({"message": "Token invalid!"}), 401

        return f(*args, **kwargs)

    return decorated


def require_json(f):
    """
    Decorator to ensure that the request content type is JSON.

    This decorator checks if the request's content type is "application/json".
    If it is not, it returns a 415 Unsupported Media Type response.
    If the request is not JSON or is invalid, it returns a 400 Bad Request response.
    Args
        f (function): The function to be decorated.
    Returns:
        function: The decorated function that checks for JSON content type.
    Raises:
        UnsupportedMediaType: If the content type is not application/json.
        BadRequest: If the request is not JSON or is invalid.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.content_type != "application/json":
            return jsonify({"message": "Content-Type must be application/json"}), 415
        if not request.is_json:
            return jsonify({"message": "JSON data is missing or invalid"}), 400
        return f(*args, **kwargs)

    return decorated


def handle_api_exceptions(default_message="Error en la operación"):
    """
    Decorator to handle exceptions in API endpoints.
    It catches ValueError, SQLAlchemyError, and general exceptions,
    returning appropriate JSON responses with error messages.
    Args:
        default_message (str): Default message for general exceptions.
    Returns:
        function: Decorated function that handles exceptions.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({"message": str(e)}), 404
            except SQLAlchemyError as e:
                return jsonify({"message": f"Database error: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"message": f"{default_message}: {str(e)}"}), 500

        return wrapper

    return decorator


def handle_logic_exceptions(default_message="Error en la operación"):
    """
    Decorator to handle exceptions in business logic functions.
    It catches ValueError, SQLAlchemyError, and general exceptions,
    raising them with a custom message.
    Args:
        default_message (str): Default message for general exceptions.
    Returns:
        function: Decorated function that handles exceptions.
    """
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ValueError as e:
                raise ValueError(f"Validation Error: {e}") from e
            except SQLAlchemyError as e:
                raise SQLAlchemyError(f"Database error: {e}") from e
            except Exception as e:
                raise Exception(f"{default_message}: {e}") from e

        return wrapper

    return decorator
