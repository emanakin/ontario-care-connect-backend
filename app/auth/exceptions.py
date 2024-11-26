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