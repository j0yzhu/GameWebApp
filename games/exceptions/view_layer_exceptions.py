"""
Contains exceptions for the view layer of the games app. Designed to automatically be caught and display an error page.
"""

from games.exceptions.base_exceptions import BaseBadRequestException, BaseNotFoundException, AbstractRequestException

class UnauthorizedException(AbstractRequestException):
    """Exception for unauthorized requests. (Invalid user input) (401)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(401, message, *args, **kwargs)

class BadRequestException(BaseBadRequestException):
    """Exception for bad requests. (Invalid user input) (400)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class NotFoundException(BaseNotFoundException):
    """Exception for not found requests. (File not found in test_repository) (404)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class GameNotFoundException(NotFoundException):
    """Exception for game not found. (File not found in test_repository) (404)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__("The game you requested could not be found", *args, **kwargs)

class GenreNotFoundException(NotFoundException):
    """Exception for genre not found. (File not found in test_repository) (404)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__("The genre you requested could not be found.", *args, **kwargs)

class BadPageNumberException(BadRequestException):
    """Exception for bad page number. (Invalid user input) (400)"""
    def __init__(self, *args, **kwargs):
        super().__init__("Invalid page number, page number must be a positive integer.", *args, **kwargs)

class BadCountException(BadRequestException):
    """Exception for bad count. (Invalid user input) (400)"""
    def __init__(self, *args, **kwargs):
        super().__init__("Invalid count, count must be a positive integer.", *args, **kwargs)

