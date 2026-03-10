from twilio.rest import Client

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID


def validate_twilio_verify_config() -> None:
    missing = []
    if not TWILIO_ACCOUNT_SID:
        missing.append("TWILIO_ACCOUNT_SID")
    if not TWILIO_AUTH_TOKEN:
        missing.append("TWILIO_AUTH_TOKEN")
    if not TWILIO_VERIFY_SERVICE_SID:
        missing.append("TWILIO_VERIFY_SERVICE_SID")

    if missing:
        raise RuntimeError(f"Missing Twilio Verify settings: {', '.join(missing)}")


def _get_client() -> Client:
    validate_twilio_verify_config()
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def _get_verify_service_sid() -> str:
    validate_twilio_verify_config()
    return TWILIO_VERIFY_SERVICE_SID


def send_otp(phone: str) -> str:
    client = _get_client()
    verification = client.verify.v2.services(_get_verify_service_sid()).verifications.create(
        to=phone,
        channel="sms",
    )
    return verification.status


def verify_otp(phone: str, code: str) -> str:
    client = _get_client()
    verification_check = client.verify.v2.services(_get_verify_service_sid()).verification_checks.create(
        to=phone,
        code=code,
    )
    return verification_check.status
