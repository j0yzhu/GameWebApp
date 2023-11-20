from games.exceptions.base_exceptions import RepositoryLayerException

class ResourceNotFoundException(RepositoryLayerException):
    """Exception for resource not found. (File not found in test_repository)"""
    def __init__(self, message: str = "The requested resource does not exist in the test_repository", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class ResourceAlreadyExistsException(RepositoryLayerException):
    """Exception for resource already existing. (File already exists in test_repository)"""
    def __init__(self, message: str = "The requested resource has a unique constraint and already exists in the test_repository", *args, **kwargs):
        super().__init__(message, *args, **kwargs)