"""
Utility functions for token validation
"""
import jwt
from datetime import datetime
from typing import Optional
from core.config import settings
from auth.jwt_handler import TokenData
import logging

logger = logging.getLogger(__name__)

def validate_token_structure(token: str) -> bool:
    """
    Validate the basic structure of a JWT token without verifying the signature
    """
    try:
        # Decode without verification to check structure
        jwt.decode(token, options={"verify_signature": False})
        return True
    except jwt.DecodeError:
        logger.warning("Invalid JWT structure")
        return False
    except Exception:
        logger.warning("Unknown error during token structure validation")
        return False

def validate_token_expiry(token: str) -> bool:
    """
    Validate that the token hasn't expired without verifying signature
    """
    try:
        # Decode without verification to check expiry
        decoded = jwt.decode(token, options={"verify_signature": False})
        exp = decoded.get('exp')

        if exp:
            if datetime.fromtimestamp(exp) < datetime.utcnow():
                logger.warning("Token has expired")
                return False
            return True
        else:
            # If no expiry claim, consider valid
            return True
    except jwt.DecodeError:
        logger.warning("Unable to decode token for expiry check")
        return False
    except Exception:
        logger.warning("Unknown error during token expiry validation")
        return False

def validate_and_decode_token(token: str) -> Optional[TokenData]:
    """
    Validate and decode the token with full verification
    """
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            logger.warning("Token does not contain user ID")
            return None

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            logger.warning("Token has expired")
            return None

        return TokenData(user_id=user_id)
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.JWTError as e:
        logger.warning(f"JWT validation error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {e}")
        return None

def is_valid_jwt_format(token: str) -> bool:
    """
    Check if the token follows JWT format (header.payload.signature)
    """
    try:
        parts = token.split('.')
        return len(parts) == 3
    except:
        return False