from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional, List, Any
from enum import Enum

T = TypeVar('T')

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class BaseResponse(BaseModel, Generic[T]):
    status: ResponseStatus
    message: str
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    metadata: Optional[dict] = None

    model_config = ConfigDict(use_enum_values=True)

class SuccessResponse(BaseResponse[T]):
    status: ResponseStatus = ResponseStatus.SUCCESS

class ErrorResponse(BaseResponse[T]):
    status: ResponseStatus = ResponseStatus.ERROR

def create_success_response(
    data: Optional[T] = None,
    message: str = "Operation completed successfully",
    metadata: Optional[dict] = None
) -> SuccessResponse[T]:
    return SuccessResponse(
        status=ResponseStatus.SUCCESS,
        message=message,
        data=data,
        metadata=metadata
    )

def create_error_response(
    message: str = "An error occurred",
    errors: Optional[List[str]] = None,
    metadata: Optional[dict] = None
) -> ErrorResponse[None]:
    return ErrorResponse(
        status=ResponseStatus.ERROR,
        message=message,
        errors=errors or [message],
        metadata=metadata
    )