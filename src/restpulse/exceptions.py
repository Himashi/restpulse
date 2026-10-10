class RestPulseError(Exception):
    """Base exception for all RestPulse errors."""
    pass

class APIError(RestPulseError):
    """Raised when the API returns an error status code (4xx, 5xx)."""
    def __init__(self, message: str, status_code: int, response_body: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class AuthenticationError(APIError):
    """Raised when authentication fails (401 Unauthorized)."""
    pass

class NotFoundError(APIError):
    """Raised when a resource is not found (404 Not Found)."""
    pass