import time  # Used for countdown timer
import secrets  # Used for secure OTP generation
import hmac  # Used for safer OTP comparison
import os  # Used to detect operating system
import sys  # Used for cross-platform keyboard reading

if os.name == "nt":
    import msvcrt  # Windows keyboard input helper
else:
    import select  # Unix non-blocking input helper
    import termios  # Unix terminal mode helper
    import tty  # Unix cbreak mode helper

OTP_LENGTH = 6  # OTP length
OTP_VALID_SECONDS = 60  # OTP valid for 60 seconds
MAX_ATTEMPTS = 3  # Maximum wrong tries before lock


def generate_otp():  # Generate secure random OTP
    return "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))  # 6 random digits


def is_valid_mobile_number(phone):  # Validate realistic mobile number format
    if not (phone.isdigit() and len(phone) == 10):  # Must be exactly 10 digits
        return False  # Invalid format
    if phone[0] not in ["6", "7", "8", "9"]:  # First digit must be 6, 7, 8, or 9
        return False  # Invalid starting digit
    if phone in {"1234567890", "0000000000"}:  # Reject known fake example numbers
        return False  # Invalid sample-like number
    if phone == phone[0] * 10:  # Reject repeated digits like 1111111111
        return False  # Invalid repeated number
    return True  # Valid mobile number


def input_otp_with_deadline(end_time):  # Read OTP while showing live countdown
    otp_text = ""  # Stores typed OTP digits
    last_remaining = -1  # Avoid duplicate timer prints

    old_settings = None  # Saved terminal settings for Unix
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)  # Read one key at a time without waiting for Enter

    try:
        while True:
            remaining = max(0, int(end_time - time.time() + 0.999))  # Seconds left (rounded)
            minutes = remaining // 60  # Minute part for MM:SS format
            seconds = remaining % 60  # Second part for MM:SS format

            if remaining != last_remaining:  # Print when second changes
                print(f"\r{minutes:02d}:{seconds:02d} | Enter OTP: {otp_text}", end="", flush=True)
                last_remaining = remaining

            if time.time() >= end_time:  # Time reached
                print()
                return None  # Return None means OTP expired

            key = None
            if os.name == "nt":
                if msvcrt.kbhit():  # Check keyboard input
                    key = msvcrt.getwch()  # Read one key
            else:
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                if readable:
                    key = sys.stdin.read(1)  # Read one key in cbreak mode

            if key is not None:
                if key in ("\r", "\n"):  # Enter key submitted
                    print()
                    return otp_text
                if key in ("\b", "\x08", "\x7f"):  # Backspace on Windows/Unix terminals
                    otp_text = otp_text[:-1]
                elif key.isdigit() and len(otp_text) < OTP_LENGTH:  # Only digits, max length
                    otp_text += key

            time.sleep(0.05)  # Prevent high CPU usage
    finally:
        if os.name != "nt" and old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)  # Restore terminal


def verify_otp_with_attempts(otp):  # Verify OTP with timer + attempt limit
    end_time = time.time() + OTP_VALID_SECONDS  # Common deadline for all tries
    attempts = 0  # Attempt counter

    while attempts < MAX_ATTEMPTS:
        user_otp = input_otp_with_deadline(end_time)  # Read OTP with countdown

        if user_otp is None:  # Timer expired
            return "expired"  # Expired status

        attempts += 1  # Count this attempt
        left = MAX_ATTEMPTS - attempts  # Attempts left after this try

        if not user_otp:  # Empty submit
            if left > 0:
                print(f"OTP cannot be empty. Attempts left: {left}")
            else:
                print("OTP cannot be empty. Attempts left: 0")
        elif len(user_otp) != OTP_LENGTH or not user_otp.isdigit():  # Must be numeric and exact length
            if left > 0:
                print(f"OTP must be {OTP_LENGTH} digits. Attempts left: {left}")
            else:
                print(f"OTP must be {OTP_LENGTH} digits. Attempts left: 0")
        elif hmac.compare_digest(user_otp, otp):  # Safer OTP comparison
            return "success"  # Success status
        else:
            if left > 0:
                print(f"Invalid OTP. Attempts left: {left}")  # Wrong OTP with remaining tries
            else:
                print("Invalid OTP. Attempts left: 0")

    return "locked"  # Too many attempts


print("OTP Secure System Started")  # Start message

while True:  # Keep asking until mobile number is valid
    phone = input("Enter mobile number: ").strip()  # Ask mobile number
    if is_valid_mobile_number(phone):  # Validate phone with extra fake-number checks
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
