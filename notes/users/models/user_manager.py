import logging

from fastapi import Request
from fastapi_users import IntegerIDMixin, BaseUserManager

from core.config import settings
from users.models.user import User

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.auth_jwt.reset_password_token_secret
    verification_token_secret = settings.auth_jwt.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ):
        log.warning(
            "User %s has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        log.warning(
            "User %s has forgot their password. Reset token: %s",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        log.warning(
            "Verification requested for user %s. Verification token: %s",
            user.id,
            token,
        )
