from fastapi import HTTPException, status, FastAPI, Request


class InvalidDataException(Exception):
    """Base exception class for input errors."""


def exception_handler(request: Request, exc: Exception):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


def add_exception_handler(app: FastAPI):
    app.add_exception_handler(InvalidDataException, exception_handler)