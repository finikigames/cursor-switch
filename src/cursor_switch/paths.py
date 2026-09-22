from __future__ import annotations

import os
import sys
from pathlib import Path

APPLICATION_USER_KEY = (
    "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl"
    ".persistentStorage.applicationUser"
)


def _env_path(name: str, default: Path) -> Path:
    override = os.environ.get(name)
    if override:
        return Path(override).expanduser()
    return default


def _default_cursor_config() -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Cursor"
    return home / ".config" / "Cursor"


def _default_cursor_cli() -> Path:
    return Path.home() / ".config" / "cursor"


def _default_root() -> Path:
    return Path.home() / ".config" / "cursor-accounts"


DEFAULT_CURSOR_CONFIG = _env_path("CURSOR_SWITCH_CONFIG_DIR", _default_cursor_config())
DEFAULT_CURSOR_HOME = _env_path("CURSOR_SWITCH_HOME_DIR", Path.home() / ".cursor")
DEFAULT_CURSOR_CLI = _env_path("CURSOR_SWITCH_CLI_DIR", _default_cursor_cli())
ROOT = _env_path("CURSOR_SWITCH_ROOT", _default_root())

SHARED_CONFIG = ROOT / "shared" / "config"
SHARED_CURSOR_HOME = ROOT / "shared" / "cursor-home"
SHARED_EXTENSIONS = SHARED_CURSOR_HOME / "extensions"
ACCOUNTS_DIR = ROOT / "accounts"
ACTIVE_FILE = ROOT / "active"
SESSION_FILE = ROOT / "session.json"
ACCOUNTS_FILE = ROOT / "accounts.toml"
LOG_FILE = ROOT / "switch.log"

STATE_DB = SHARED_CONFIG / "User" / "globalStorage" / "state.vscdb"
STORAGE_JSON = SHARED_CONFIG / "User" / "globalStorage" / "storage.json"
CODE_LOCK = SHARED_CONFIG / "code.lock"
CLI_CONFIG = SHARED_CURSOR_HOME / "cli-config.json"
STATSIG_CACHE = SHARED_CURSOR_HOME / "statsig-cache.json"
CLI_AUTH_JSON = DEFAULT_CURSOR_CLI / "auth.json"
CLI_PROMPT_HISTORY = DEFAULT_CURSOR_CLI / "prompt_history.json"

# Not swapped — cache / install artifacts (documented in docs/data-locations.md)
if sys.platform == "darwin":
    CURSOR_AGENT_DIR = Path.home() / ".local" / "share" / "cursor-agent"
    CURSOR_COMPILE_CACHE = Path.home() / "Library" / "Caches" / "cursor-compile-cache"
else:
    CURSOR_AGENT_DIR = Path.home() / ".local" / "share" / "cursor-agent"
    CURSOR_COMPILE_CACHE = Path.home() / ".cache" / "cursor-compile-cache"
CURSOR_SERVER_DIR = Path.home() / ".cursor-server"


def cursor_config_label() -> str:
    if sys.platform == "darwin":
        return "~/Library/Application Support/Cursor"
    return "~/.config/Cursor"


def session_bundle_dir(account: str) -> Path:
    return ACCOUNTS_DIR / account / "session-bundle"


def is_initialized() -> bool:
    return SHARED_CONFIG.is_dir() and ACCOUNTS_FILE.exists()


def ensure_root() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    ACCOUNTS_DIR.mkdir(parents=True, exist_ok=True)


def resolve_cursor_binary() -> str:
    candidates: list[str | None] = [os.environ.get("CURSOR_SWITCH_CURSOR_BIN")]
    if sys.platform == "darwin":
        candidates.extend(
            [
                "/Applications/Cursor.app/Contents/Resources/app/bin/cursor",
                str(Path.home() / ".local/bin/cursor"),
                "/usr/local/bin/cursor",
            ]
        )
    else:
        candidates.extend(
            [
                "/usr/share/cursor/bin/cursor",
                str(Path.home() / ".local/bin/cursor"),
            ]
        )
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    return "cursor"
