from otp_service import generate_otp, verify_otp_with_attempts
from validators import is_valid_mobile_number


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
