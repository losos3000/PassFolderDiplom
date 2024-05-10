from fastapi import Depends
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from database.db_connect import AccessToken, get_access_token_db

SECRET = "SECRET"

cookie_transport = CookieTransport(cookie_name="user", cookie_max_age=3600)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="db",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

