from input_handler import input_mobile_with_panel, input_yes_no_with_panel
from otp_service import generate_otp, verify_otp_with_attempts
from ui import show_prompt_panel
from validators import is_valid_mobile_number


mobile_status = ""
while True:  # Keep asking until mobile number is valid
    phone = input_mobile_with_panel("Enter mobile number:", mobile_status)  # Ask mobile number
    if is_valid_mobile_number(phone):  # Validate phone with extra fake-number checks
        break  # Exit loop when valid number is entered
    mobile_status = "Please enter a valid mobile number"

otp = generate_otp()  # Generate secure random OTP
result = verify_otp_with_attempts(otp, phone, show_demo_otp=True)  # First OTP verification flow

if result == "success":  # Login success
    show_prompt_panel(phone, "Session Complete", "", "Login Successful")
elif result == "locked":  # Too many attempts
    show_prompt_panel(phone, "Session Complete", "", "Account locked")
else:
    resend_choice = input_yes_no_with_panel(phone, "Time limit reached. Resend OTP? (yes/no)")

    if resend_choice == "yes":  # Resend requested
        otp = generate_otp()  # Generate new OTP
        result = verify_otp_with_attempts(otp, phone, show_demo_otp=True)  # Verify new OTP

        if result == "success":  # New OTP correct
            show_prompt_panel(phone, "Session Complete", "", "Login Successful")
        elif result == "locked":  # Too many tries on new OTP
            show_prompt_panel(phone, "Session Complete", "", "Account locked")
        else:
            show_prompt_panel(phone, "Session Complete", "", "OTP expired again")
    elif resend_choice == "no":  # User does not want resend
        show_prompt_panel(phone, "Session Complete", "", "Session ended. Have a nice day!!")
    else:
        show_prompt_panel(phone, "Session Complete", "", "Invalid choice. Type yes or no.")
