from enum import Enum


class StatusCodes(Enum):
    # Успешные
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # Ошибки клиента
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    CONFLICT = 409

    # Ошибки сервера
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILIBLE = 503
