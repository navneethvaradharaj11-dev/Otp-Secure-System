import hmac
import secrets
import time

from config import MAX_ATTEMPTS, OTP_LENGTH, OTP_VALID_SECONDS
from input_handler import input_otp_with_deadline


def generate_otp():
    return "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))


def is_otp_match(user_otp, otp):
    return hmac.compare_digest(user_otp, otp)


def verify_otp_with_attempts(otp):
    end_time = time.time() + OTP_VALID_SECONDS
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        user_otp = input_otp_with_deadline(end_time)

        if user_otp is None:
            return "expired"

        attempts += 1
        left = MAX_ATTEMPTS - attempts

        if not user_otp:
            if left > 0:
                print(f"OTP cannot be empty. Attempts left: {left}")
            else:
                print("OTP cannot be empty. Attempts left: 0")
        elif len(user_otp) != OTP_LENGTH or not user_otp.isdigit():
            if left > 0:
                print(f"OTP must be {OTP_LENGTH} digits. Attempts left: {left}")
            else:
                print(f"OTP must be {OTP_LENGTH} digits. Attempts left: 0")
        elif is_otp_match(user_otp, otp):
            return "success"
        else:
            if left > 0:
                print(f"Invalid OTP. Attempts left: {left}")
            else:
                print("Invalid OTP. Attempts left: 0")

    return "locked"
