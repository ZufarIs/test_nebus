from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(
    api_key: str = Security(api_key_header)
) -> str:
    """
    Проверить API ключ.
    
    Args:
        api_key (str): API ключ из заголовка запроса
        
    Returns:
        str: Проверенный API ключ
        
    Raises:
        HTTPException: Если API ключ неверный
    """
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API key"
        )
    return api_key 
