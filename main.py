import logging
import sys
import time

from config import OTP_VALID_SECONDS, SHOW_DEMO_OTP
from input_handler import input_mobile_with_panel, input_yes_no_with_panel
from otp_service import OTPSession, OtpVerificationResult, verify_otp_with_attempts
from twilio.base.exceptions import TwilioRestException
from twilio_service import send_otp, validate_twilio_verify_config, verify_otp
from ui import show_prompt_panel
from validators import format_phone_number, is_valid_mobile_number

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="otp_app.log",
    filemode="a",
    force=True,
)
logger = logging.getLogger(__name__)


def _show_fatal_error(phone: str, message: str) -> None:
    show_prompt_panel(phone, "Session Complete", "", message)
    sys.exit(1)


mobile_status = ""
logger.info("OTP app started")
while True:  # Keep asking until mobile number is valid
    phone = input_mobile_with_panel("Enter mobile number:", mobile_status)  # Ask mobile number
    if is_valid_mobile_number(phone):  # Validate phone with extra fake-number checks
        phone = format_phone_number(phone)
        logger.info("Valid mobile number accepted")
        break  # Exit loop when valid number is entered
    logger.warning("Invalid mobile number entered")
    mobile_status = "Please enter a valid mobile number"

session = OTPSession(phone)
if SHOW_DEMO_OTP:
    otp = session.issue_new_otp()  # Generate secure random OTP
    logger.warning("SHOW_DEMO_OTP is enabled; OTP will be visible in console")
    print("OTP:", otp)
else:
    try:
        validate_twilio_verify_config()
    except RuntimeError as exc:
        logger.exception("Twilio Verify configuration is incomplete")
        _show_fatal_error(phone, str(exc))
    session.expiry = time.time() + OTP_VALID_SECONDS
    session.attempts = 0
try:
    send_status = send_otp(phone) if not SHOW_DEMO_OTP else "demo"
    logger.info("OTP send request completed. status=%s", send_status)
except TwilioRestException as exc:
    logger.exception("Twilio Verify request failed")
    _show_fatal_error(phone, f"Twilio error {exc.code}: {exc.msg}")
except Exception:
    logger.exception("Failed to send OTP SMS")
    _show_fatal_error(phone, "Unable to send OTP right now. Check Twilio configuration.")
result = verify_otp_with_attempts(
    session,
    verify_callback=verify_otp,
    show_demo_otp=SHOW_DEMO_OTP,
)  # First OTP verification flow

if result == OtpVerificationResult.SUCCESS:  # Login success
    logger.info("Session completed successfully")
    show_prompt_panel(phone, "Session Complete", "", "Verification successful. You are now signed in.")
elif result == OtpVerificationResult.LOCKED:  # Too many attempts
    logger.error("Session locked after too many incorrect attempts")
    show_prompt_panel(phone, "Session Complete", "", "Too many incorrect attempts. This session is now locked.")
else:
    logger.warning("OTP expired; prompting resend choice")
    resend_status = "Type yes or no, then press Enter."
    while True:
        resend_choice = input_yes_no_with_panel(
            phone,
            "Your code has expired. Resend a new OTP? (yes/no)",
            resend_status,
        )
        if resend_choice in {"yes", "no"}:
            logger.info("Resend choice captured: %s", resend_choice)
            break
        logger.warning("Invalid resend choice entered")
        resend_status = "Invalid choice. Please type only yes or no."

    if resend_choice == "yes":  # Resend requested
        logger.info("User requested OTP resend")
        if SHOW_DEMO_OTP:
            otp = session.issue_new_otp()  # Generate new OTP
            logger.warning("SHOW_DEMO_OTP is enabled; resent OTP will be visible in console")
            print("OTP:", otp)
        else:
            session.expiry = time.time() + OTP_VALID_SECONDS
            session.attempts = 0
        try:
            send_status = send_otp(phone) if not SHOW_DEMO_OTP else "demo"
            logger.info("Resend OTP request completed. status=%s", send_status)
        except TwilioRestException as exc:
            logger.exception("Twilio Verify resend failed")
            _show_fatal_error(phone, f"Twilio error {exc.code}: {exc.msg}")
        except Exception:
            logger.exception("Failed to send resend OTP SMS")
            _show_fatal_error(phone, "Unable to resend OTP right now. Check Twilio configuration.")
        result = verify_otp_with_attempts(
            session,
            verify_callback=verify_otp,
            show_demo_otp=SHOW_DEMO_OTP,
        )  # Verify new OTP

        if result == OtpVerificationResult.SUCCESS:  # New OTP correct
            logger.info("Session completed successfully after resend")
            show_prompt_panel(phone, "Session Complete", "", "Verification successful. You are now signed in.")
        elif result == OtpVerificationResult.LOCKED:  # Too many tries on new OTP
            logger.error("Session locked after resend verification attempts")
            show_prompt_panel(phone, "Session Complete", "", "Too many incorrect attempts. This session is now locked.")
        else:
            logger.warning("Resent OTP expired")
            show_prompt_panel(phone, "Session Complete", "", "The new OTP also expired. Please try again later.")
    elif resend_choice == "no":  # User does not want resend
        logger.info("User canceled verification after OTP expiry")
        show_prompt_panel(phone, "Session Complete", "", "Verification canceled. You can request a new OTP anytime.")
