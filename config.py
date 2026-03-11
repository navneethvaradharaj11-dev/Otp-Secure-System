import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None


def _load_local_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


ENV_PATH = Path(__file__).resolve().parent / ".env"
if load_dotenv is not None:
    load_dotenv(dotenv_path=ENV_PATH)
else:
    _load_local_env_file(ENV_PATH)

OTP_LENGTH = 6
OTP_VALID_SECONDS = 60
MAX_ATTEMPTS = 3
SHOW_DEMO_OTP = False

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_VERIFY_SERVICE_SID = os.getenv("TWILIO_VERIFY_SERVICE_SID", "")
