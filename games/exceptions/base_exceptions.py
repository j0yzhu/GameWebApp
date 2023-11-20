from abc import ABC

class RepositoryLayerException(Exception, ABC):
    """Abstract class for test_repository layer exceptions."""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

class ServiceLayerException(Exception, ABC):
    """Abstract class for service layer exceptions."""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

class AbstractRequestException(Exception, ABC):
    """Abstract class for request exceptions."""
    def __init__(self, status_code: int, message: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code
        self.message = message

class BaseBadRequestException(AbstractRequestException):
    """Exception for bad requests. (Invalid user input) (400)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(400, message, *args, **kwargs)

class BaseNotFoundException(AbstractRequestException):
    """Exception for not found requests. (File not found in test_repository) (404)"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(404, message, *args, **kwargs)