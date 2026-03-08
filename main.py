import time  # Used for countdown timer
import secrets  # Used for secure OTP generation
import hmac  # Used for safer OTP comparison
import msvcrt  # Windows-only keyboard input helper

OTP_LENGTH = 6  # OTP length
OTP_VALID_SECONDS = 60  # OTP valid for 60 seconds
MAX_ATTEMPTS = 3  # Maximum wrong tries before lock


def generate_otp():  # Generate secure random OTP
    return "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))  # 6 random digits


def input_otp_with_deadline(end_time):  # Read OTP while showing live countdown
    otp_text = ""  # Stores typed OTP digits
    last_remaining = -1  # Avoid duplicate timer prints

    while True:
        remaining = int(end_time - time.time())  # Seconds left

        if remaining != last_remaining and remaining >= 0:  # Print when second changes
            print(f"\rTimer: {remaining}s | Enter OTP: {otp_text}", end="", flush=True)  # Live timer line
            last_remaining = remaining  # Save last shown second

        if remaining < 0:  # Time reached
            print()  # Move to next line
            return None  # Return None means OTP expired

        if msvcrt.kbhit():  # Check keyboard input
            key = msvcrt.getwch()  # Read one key

            if key in ("\r", "\n"):  # Enter key submitted
                print()  # Move to next line
                return otp_text  # Return entered OTP
            if key == "\b":  # Backspace pressed
                otp_text = otp_text[:-1]  # Remove last character
            elif key.isdigit() and len(otp_text) < OTP_LENGTH:  # Only digits, max 6
                otp_text += key  # Add typed digit

        time.sleep(0.05)  # Prevent high CPU usage


def verify_otp_with_attempts(otp):  # Verify OTP with timer + attempt limit
    end_time = time.time() + OTP_VALID_SECONDS  # Common deadline for all tries
    attempts = 0  # Attempt counter

    while attempts < MAX_ATTEMPTS:
        user_otp = input_otp_with_deadline(end_time)  # Read OTP with countdown

        if user_otp is None:  # Timer expired
            return "expired"  # Expired status

        attempts += 1  # Count this attempt

        if not user_otp:  # Empty submit
            print("OTP cannot be empty")  # Empty OTP message
        elif len(user_otp) != OTP_LENGTH:  # Short/long OTP submit
            print(f"OTP must be {OTP_LENGTH} digits")  # Strict OTP length check
        elif hmac.compare_digest(user_otp, otp):  # Safer OTP comparison
            return "success"  # Success status
        else:
            left = MAX_ATTEMPTS - attempts  # Attempts left
            if left > 0:
                print(f"Invalid OTP. Attempts left: {left}")  # Wrong OTP with remaining tries

    return "locked"  # Too many attempts


print("OTP Secure System Started")  # Start message

while True:  # Keep asking until phone number is valid
    phone = input("Enter phone number: ").strip()  # Ask phone number
    if phone.isdigit() and len(phone) == 10:  # Validate phone (exactly 10 digits)
        break  # Exit loop when valid number is entered
    print("Please enter a valid mobile number")  # Empty/invalid phone input

otp = generate_otp()  # Generate secure random OTP
print("OTP sent to", phone, ":", otp)  # Show OTP for demo
result = verify_otp_with_attempts(otp)  # First OTP verification flow

if result == "success":  # Login success
    print("Login Successful")  # Correct OTP
elif result == "locked":  # Too many attempts
    print("Account locked")  # Lock message
else:
    print("Time limit reached resend OTP?")  # Expiry message
    resend_choice = input("Type yes or no: ").strip().lower()  # Ask resend option

    if resend_choice == "yes":  # Resend requested
        otp = generate_otp()  # Generate new OTP
        print("New OTP sent to", phone, ":", otp)  # Show new OTP for demo
        result = verify_otp_with_attempts(otp)  # Verify new OTP

        if result == "success":  # New OTP correct
            print("Login Successful")  # Login success
        elif result == "locked":  # Too many tries on new OTP
            print("Account locked")  # Lock message
        else:
            print("OTP expired again")  # New OTP expired too
    elif resend_choice == "no":  # User does not want resend
        print("Session ended")  # Session is closed when user skips resend
        print("Have a nice day!!")  # Exit message
    else:
        print("Invalid choice. Type yes or no.")  # Wrong yes/no input
