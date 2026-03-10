from twilio_service import send_otp, verify_otp


def main() -> None:
    phone = "+919994138347"  # Replace with a phone number allowed by your Twilio setup.
    send_status = send_otp(phone)
    print(f"OTP send status: {send_status}")

    code = input("Enter the OTP you received: ").strip()
    result = verify_otp(phone, code)
    print(f"Verification status: {result}")

    if result == "approved":
        print("OTP verified")
    else:
        print("Invalid OTP")


if __name__ == "__main__":
    main()
