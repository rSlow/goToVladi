from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from goToVladi.core.data.db import models as db
from goToVladi.core.utils.auth import SecurityService
from goToVladi.core.utils import exceptions as exc


class AuthService:
    def __init__(self, security: SecurityService):
        self.security = security

    def authenticate_user(
            self, username: str, password: str, session: Session,
    ):
        result = session.scalars(
            select(db.User)
            .where(db.User.username == username)
        )
        try:
            user = result.one()
        except (MultipleResultsFound, NoResultFound):
            raise exc.InvalidCredentialsError
        if not self.security.pwd_context.verify(password, user.hashed_password):
            raise exc.InvalidCredentialsError
        if not user.is_superuser or user.id is None:
            raise exc.AccessDeniedError
        return user
