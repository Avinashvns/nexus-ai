from sqlalchemy import select

from database.models.user import User
from database.session import SessionLocal


class UserRepository:
    
    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        with SessionLocal() as session:
            statement = select(User).where(User.id == user_id)

            user = session.scalar(statement)

            if user is not None:
                session.expunge(user)

            return user

    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        with SessionLocal() as session:
            statement = select(User).where(User.username == username)

            return session.scalar(statement)

    def create(
        self,
        username: str,
        hashed_password: str,
    ) -> User:
        with SessionLocal() as session:
            user = User(
                username=username,
                hashed_password=hashed_password,
            )

            session.add(user)

            session.commit()

            session.refresh(user)

            session.expunge(user)

            return user


user_repository = UserRepository()
