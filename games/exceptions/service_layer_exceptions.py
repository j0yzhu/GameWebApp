from games.exceptions.base_exceptions import ServiceLayerException

class ResourceNotFoundException(ServiceLayerException):
    """Exception for resource not found. (File not found in test_repository)"""
    def __init__(self, message: str = "The requested resource could not be found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class ResourceAlreadyExistsException(ServiceLayerException):
    """Exception for resource already existing. (File already exists in test_repository)"""
    def __init__(self, message: str = "The requested resource already exists and is not allowed duplicates", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class AuthenticationException(ServiceLayerException):
    """Exception for authentication failure."""
    def __init__(self, message: str = "Authentication failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class AuthorizationException(ServiceLayerException):
    """Exception for authorization failure."""
    def __init__(self, message: str = "Authorization failed", *args, **kwargs):
        super().__init__(message, *args, **kwargs)