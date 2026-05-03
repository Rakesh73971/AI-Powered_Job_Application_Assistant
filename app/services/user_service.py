from sqlalchemy.orm import Session
from app.models.user import User
from app.core.utils import hash_password


def create_user(db:Session,user):
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
