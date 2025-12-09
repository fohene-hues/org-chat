from typing import List, Optional

from sqlmodel import Session, select
from passlib.context import CryptContext

from ..model.user import User, Role, Permission, RolePermissionLink
from .schemas import UserCreate, RoleCreate, PermissionCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# user
def create_user(db: Session, user_in: UserCreate) -> User:
    hashed = pwd_context.hash(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        name=user_in.name,
        department=user_in.department,
        hashed_password=hashed,
        role_id=user_in.role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = db.exec(statement).first()
    return result


# role + permission helpers
def create_permission(db: Session, p_in: PermissionCreate) -> Permission:
    perm = Permission(name=p_in.name, description=p_in.description)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def create_role(db: Session, r_in: RoleCreate) -> Role:
    role = Role(name=r_in.name, description=r_in.description)
    db.add(role)
    db.commit()
   
    if r_in.permission_ids:
        perms = db.exec(select(Permission).where(Permission.id.in_(r_in.permission_ids))).all()
        role.permissions = perms
        db.add(role)
        db.commit()
        db.refresh(role)
    return role
