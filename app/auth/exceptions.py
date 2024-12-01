class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists.")

class InvalidRoleException(Exception):
    def __init__(self, role: str):
        self.role = role
        super().__init__(f"Role '{role}' is not permitted for signup.")

class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Incorrect email or password.")

class InvalidTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid token.")

class UnapprovedCaregiverException(Exception):
    def __init__(self):
        super().__init__("Caregiver account not approved.")

class EmailAlreadyVerifiedException(Exception):
    """Raised when the user's email is already verified."""
    def __init__(self, detail: str = "Email is already verified"):
        self.detail = detail
        super().__init__(self.detail)

class UserNotFoundException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' not found.")

class InvalidAuthProviderException(Exception):
    def __init__(self, message: str = "Invalid authentication provider."):
        super().__init__(message)

class EmailNotVerifiedException(Exception):
    def __init__(self, message: str = "Email address is not verified."):
        super().__init__(message)
