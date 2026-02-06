"""
Simple test file to validate JWT token scenarios
"""
import jwt
import pytest
from datetime import datetime, timedelta
from core.config import settings
from auth.jwt_handler import decode_jwt_token, get_current_user
from utils.token_validator import validate_and_decode_token


def create_test_token(user_id: str = "test_user", expires_delta: timedelta = timedelta(hours=1)):
    """Create a test JWT token"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


def test_valid_token():
    """Test a valid token"""
    token = create_test_token()
    result = validate_and_decode_token(token)
    assert result is not None
    assert result.user_id == "test_user"


def test_expired_token():
    """Test an expired token"""
    token = create_test_token(expires_delta=timedelta(seconds=-1))  # Expired token
    result = validate_and_decode_token(token)
    assert result is None


def test_invalid_secret_token():
    """Test a token with wrong secret"""
    # Create token with different secret
    payload = {
        "sub": "test_user",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, "wrong_secret", algorithm="HS256")
    result = validate_and_decode_token(token)
    assert result is None


def test_malformed_token():
    """Test a malformed token"""
    result = validate_and_decode_token("malformed.token.string")
    assert result is None


if __name__ == "__main__":
    print("Testing JWT validation scenarios...")

    # Run tests
    test_valid_token()
    print("✓ Valid token test passed")

    test_expired_token()
    print("✓ Expired token test passed")

    test_invalid_secret_token()
    print("✓ Invalid secret token test passed")

    test_malformed_token()
    print("✓ Malformed token test passed")

    print("\nAll JWT validation tests passed!")