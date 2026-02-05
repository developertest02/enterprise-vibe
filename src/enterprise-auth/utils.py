import bcrypt
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserRegistrationRequest(BaseModel):
    """Pydantic model for user registration request"""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=8, description="User's password")
    first_name: Optional[str] = Field(None, max_length=255, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=255, description="User's last name")
    display_name: Optional[str] = Field(None, max_length=255, description="User's display name")

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be at most 50 characters long')

        # Check for valid characters (alphanumeric and underscore/hyphen)
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain alphanumeric characters, underscores, and hyphens')

        return v.lstrip().rstrip()  # strip whitespace

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Check for complexity: at least one uppercase, lowercase, digit
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')

        return v

    @validator('email')
    def validate_email_format(cls, v):
        # EmailStr validation already handles basic format, but we can add additional validation
        # Check for common disposable email providers
        domain = v.split('@')[1].lower() if '@' in v else ''
        disposable_domains = [
            'guerrillamail.com', 'temp-mail.org', 'mailinator.com',
            'throwawaymail.com', '10minutemail.com'
        ]

        if domain in disposable_domains:
            raise ValueError('Disposable email addresses are not allowed')

        return v