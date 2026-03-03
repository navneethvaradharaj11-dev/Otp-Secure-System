# OTP Secure System Simulation
import random

def generate_otp():
    return random.randint(100000, 999999)

print("OTP Secure System Started")

phone = input("Enter phone number: ")

otp = generate_otp()

print(f"[SIMULATION] OTP sent to {phone}: {otp}")

try:
    user_input = int(input("Enter received OTP: "))

    if user_input == otp:
        print("Login Successful 🎉")
    else:
        print("Invalid OTP ❌")

except ValueError:
    print("Please enter numbers only ❗")

