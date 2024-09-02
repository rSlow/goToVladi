import base64
import logging
import typing
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Request
from jwt import PyJWTError as JWTError
from passlib.context import CryptContext
from starlette import status

from goToVladi.api.config.models.auth import AuthConfig
from goToVladi.api.config.models.auth.token import Token
from goToVladi.core.data.db import dto
from goToVladi.core.data.db.dao import DaoHolder
from goToVladi.core.utils.exceptions.user import NoUsernameFound
from goToVladi.core.utils.tz import tz_utc

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, config: AuthConfig) -> None:
        super().__init__()
        self.config = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = config.secret_key
        self.algorythm = config.algorythm
        self.access_token_expire = config.token_expire

    def _verify_password(
            self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(
            self, username: str, password: str,
            dao: DaoHolder
    ) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            user = await dao.user.get_by_username_with_password(username)
        except NoUsernameFound as e:
            raise http_status_401 from e
        if not self._verify_password(password, user.hashed_password or ""):
            raise http_status_401
        return user.without_password()

    def create_access_token(self, data: dict,
                            expires_delta: timedelta) -> Token:
        to_encode = data.copy()
        expire = datetime.now(tz=tz_utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorythm
        )
        return Token(token=encoded_jwt, token_type="bearer")

    def create_user_token(self, user: dto.User) -> Token:
        return self.create_access_token(
            data={"sub": str(user.db_id)},
            expires_delta=self.access_token_expire
        )

    async def get_current_user(
            self, token: Token, dao: DaoHolder,
    ) -> dto.User:
        logger.debug("try to check token %s", token)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jwt.decode(
                token.token,
                key=self.secret_key,
                algorithms=[self.algorythm],
            )
            if payload.get("sub") is None:
                logger.warning("valid jwt contains no user id")
                raise credentials_exception
            user_db_id = int(typing.cast(str, payload.get("sub")))

        except JWTError as e:
            logger.info("invalid jwt", exc_info=e)
            raise credentials_exception from e

        except Exception as e:
            logger.warning("some jwt error", exc_info=e)
            raise e

        try:
            user = await dao.user.get_by_tg_id(user_db_id)
        except Exception as e:
            logger.info("user by id %s not found", user_db_id)
            raise credentials_exception from e

        return user

    async def get_user_basic(
            self, request: Request, dao: DaoHolder
    ) -> dto.User | None:
        if (header := request.headers.get("Authorization")) is None:
            return None

        schema, token = header.split(" ", maxsplit=1)
        if schema.lower() != "basic":
            return None
        decoded = base64.urlsafe_b64decode(token).decode("utf-8")
        username, password = decoded.split(":", maxsplit=1)
        return await self.authenticate_user(username, password, dao)
