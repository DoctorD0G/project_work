from typing import Dict

from fastapi import status
from fastapi.exceptions import HTTPException


class FormFieldValidationException(HTTPException):
    fields = None

    def __init__(self, fields: Dict, *args, **kwargs):
        super().__init__(
            *args, **kwargs, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.fields = fields
