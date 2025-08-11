import os
from typing import Annotated
from fastapi import ( HTTPException,
                     status,
                     Security,
                     )
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("API_KEY")  # Single API key for simplicity

if not API_KEY:
    raise ValueError(
        "API_KEY environment variable not set. Please set it in your .env file or environment."
    )

# Define the security scheme: Expect an API key in a header named "X-API-Key"
api_key_header = APIKeyHeader(
    name="X-API-Key", auto_error=True
)  # auto_error=True will automatically raise 403 if header is missing


# --- Dependency to validate the API Key ---
async def get_api_key(api_key: Annotated[str, Security(api_key_header)]):
    """
    Dependency function to validate the API key from the header.
    """
    if api_key == API_KEY:
        return api_key  # Return the key or a user object associated with it
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "X-API-Key"},
        )
