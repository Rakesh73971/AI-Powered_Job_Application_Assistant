from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_access_token(
    token: str,
    credentials_exception: HTTPException
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=int(user_id))

        return token_data

    except JWTError:
        raise credentials_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify JWT
    token_data = verify_access_token(
        token,
        credentials_exception
    )

    # Async database query
    result = await db.execute(
        select(User).where(User.id == token_data.id)
    )

    # Get User object
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:

    role_value = (
        current_user.role.value
        if hasattr(current_user.role, "value")
        else current_user.role
    )

    if role_value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough privileges"
        )

    return current_user