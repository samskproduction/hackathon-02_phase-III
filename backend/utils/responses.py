from typing import Any, Dict, Optional
from fastapi import HTTPException, status

def create_success_response(data: Any = None, message: str = "Operation successful") -> Dict:
    '''Create a standardized success response according to API contract'''
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def create_error_response(error_code: str, message: str, status_code: int = 400) -> Dict:
    '''Create a standardized error response according to API contract'''
    return {
        "success": False,
        "error": {
            "code": error_code,
            "message": message
        }
    }

class CustomHTTPException(HTTPException):
    '''Custom HTTP exception with standardized error format'''
    def __init__(self, error_code: str, detail: str, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail=create_error_response(error_code, detail, status_code)
        )
