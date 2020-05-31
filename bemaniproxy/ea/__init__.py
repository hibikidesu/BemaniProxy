from .game_ver import get_version_string
from .common import *
from enum import Enum

__all__ = [
    "get_version_string",
    "generate_card",
    "generate_message_maint",
    "generate_header",
    "MODULES",
    "Status"
]

MODULES = [
    "cardmng",
    "facility",
    "message",
    "numbering",
    "package",
    "pcbevent",
    "pcbtracker",
    "pkglist",
    "posevent",
    "userdata",
    "userid",
    "eacoin",
    "dlstatus",
    "posevent",
    "local",
    "local2",
    "lobby",
    "lobby2",
    "KFC"
]


class Status(Enum):
    SUCCESS = 0
    ERROR = 1
    NO_PROFILE = 109
    NOT_ALLOWED = 110
    NOT_REGISTERED = 112
    INVALID_PIN = 116
