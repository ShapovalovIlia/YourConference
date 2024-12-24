__all__ = [
    "auth_router",
    "conference_router",
    "review_router",
    "registration_router",
]

from .auth import auth_router
from .conference import conference_router
from .review import review_router
from .registration import registration_router
