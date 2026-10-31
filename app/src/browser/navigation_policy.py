import re
from enum import Enum, auto
from urllib.parse import urlsplit

TRUSTED_DOMAINS = ("youtube.com", "youtu.be", "youtube-nocookie.com")
TRUSTED_SIGN_IN_HOSTS = frozenset({
    "consent.google.com",
    "myaccount.google.com",
    "accounts.youtube.com",
})
GOOGLE_ACCOUNTS_HOST_PATTERN = re.compile(r"^accounts\.google\.(com|(com?\.)?[a-z]{2})$")
SECURE_SCHEME = "https"
EXTERNAL_SCHEMES = frozenset({"http", "https"})
EMBEDDED_FRAME_SCHEMES = frozenset({"https", "about", "blob", "data"})


class NavigationDecision(Enum):
    ALLOW = auto()
    OPEN_EXTERNALLY = auto()
    BLOCK = auto()


def decide_main_frame_navigation(url: str, user_initiated: bool) -> NavigationDecision:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme == SECURE_SCHEME and is_trusted_host(parts.hostname or ""):
        return NavigationDecision.ALLOW
    if user_initiated and scheme in EXTERNAL_SCHEMES and parts.hostname:
        return NavigationDecision.OPEN_EXTERNALLY
    return NavigationDecision.BLOCK


def decide_embedded_frame_navigation(url: str) -> NavigationDecision:
    scheme = urlsplit(url).scheme.lower()
    return NavigationDecision.ALLOW if scheme in EMBEDDED_FRAME_SCHEMES else NavigationDecision.BLOCK


def is_trusted_host(host: str) -> bool:
    normalized = host.lower().rstrip(".")
    if normalized in TRUSTED_SIGN_IN_HOSTS or GOOGLE_ACCOUNTS_HOST_PATTERN.match(normalized):
        return True
    return any(normalized == domain or normalized.endswith(f".{domain}") for domain in TRUSTED_DOMAINS)
