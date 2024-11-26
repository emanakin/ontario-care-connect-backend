from passlib.context import CryptContext
import bcrypt
print(bcrypt.__version__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashed_password = "$2b$12$ml1ZtVvXgOWj.NWuwzuHeOXg6iOpzVxYI1nnHZQzGt5DRh5dNPF8u"  
# hashed_password = "$2b$12$KQm34y070QyFwuOwFwP36OaApMCMxPsoLenKSErdCgsFvuzHYkOV."  
hashed_password = "$2b$12$oy4tlo36zXVz7CY/83swNO2/UIlZqSZ9WWwpfJ1uMwptrbmd9Joqe"  
# hashed_password = "$2b$12$g3NK810OAPL34PAxoiUeR..SJXq09qHeu3gxqOtmn76cxtZstnG22"  
plain_password = "securepassword"  # Replace with the plain password you used during signup

# new_hashed = pwd_context.hash(plain_password)
# print(f"New Hashed Password: {new_hashed}")

# Test verification
is_valid = pwd_context.verify(plain_password, hashed_password)
print(f"Password valid: {is_valid}")  # Should print True if verification works
