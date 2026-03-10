import hmac
import logging
import secrets
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from config import MAX_ATTEMPTS, OTP_LENGTH, OTP_VALID_SECONDS
from input_handler import input_otp_with_deadline

logger = logging.getLogger(__name__)


class OtpVerificationResult(str, Enum):
    """Possible OTP verification outcomes."""

    SUCCESS = "success"
    EXPIRED = "expired"
    LOCKED = "locked"


@dataclass
class OTPSession:
    """Represents OTP state for one mobile verification session."""

    phone: str
    attempts: int = 0
    otp: Optional[str] = None
    expiry: Optional[float] = None

    @property
    def masked_phone(self) -> str:
        """Return a masked phone string for logs."""
        return f"******{self.phone[-4:]}" if len(self.phone) >= 4 else self.phone

    def issue_new_otp(self) -> str:
        """Generate and attach a new OTP with fresh expiry and reset attempts."""
        self.otp = generate_otp()
        self.expiry = time.time() + OTP_VALID_SECONDS
        self.attempts = 0
        logger.info("OTP issued for %s", self.masked_phone)
        return self.otp


def generate_otp() -> str:
    """Generate a secure random numeric OTP of configured length."""
    otp = "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))
    logger.info("OTP generated")
    return otp


def is_otp_match(user_otp: str, otp: str) -> bool:
    """Constant-time OTP equality check."""
    return hmac.compare_digest(user_otp, otp)


def verify_otp_with_attempts(
    session: OTPSession,
    verify_callback: Optional[Callable[[str, str], str]] = None,
    show_demo_otp: bool = False,
) -> OtpVerificationResult:
    """Verify user OTP input for a session within expiry and attempt limits."""
    if session.expiry is None:
        session.expiry = time.time() + OTP_VALID_SECONDS
        session.attempts = 0
        logger.info("OTP session started for %s", session.masked_phone)

    if show_demo_otp and (session.otp is None or session.expiry is None):
        session.issue_new_otp()

    end_time = session.expiry
    status_text = f"Demo OTP: {session.otp}" if show_demo_otp else "A one-time code was sent to your mobile number."
    logger.info("OTP verification started for %s", session.masked_phone)

    while session.attempts < MAX_ATTEMPTS:
        user_otp = input_otp_with_deadline(end_time, session.phone, status_text)

        if user_otp is None:
            logger.warning("OTP verification expired for %s", session.masked_phone)
            return OtpVerificationResult.EXPIRED

        session.attempts += 1
        left = MAX_ATTEMPTS - session.attempts

        if not user_otp:
            logger.warning("Empty OTP submitted. Attempts remaining: %d", left)
            status_text = f"Please enter the verification code. Attempts remaining: {left}"
        elif len(user_otp) != OTP_LENGTH or not user_otp.isdigit():
            logger.warning("Invalid OTP format submitted. Attempts remaining: %d", left)
            status_text = f"Enter the {OTP_LENGTH}-digit code sent to your mobile. Attempts remaining: {left}"
        else:
            if show_demo_otp:
                is_valid = session.otp is not None and is_otp_match(user_otp, session.otp)
            elif verify_callback is not None:
                is_valid = verify_callback(session.phone, user_otp) == "approved"
            else:
                raise RuntimeError("verify_callback is required when SHOW_DEMO_OTP is disabled.")

            if is_valid:
                logger.info("OTP verified successfully for %s", session.masked_phone)
                return OtpVerificationResult.SUCCESS

            logger.warning("Incorrect OTP submitted. Attempts remaining: %d", left)
            status_text = f"The code you entered is incorrect. Attempts remaining: {left}"

    logger.error("OTP verification locked due to max attempts for %s", session.masked_phone)
    return OtpVerificationResult.LOCKED
