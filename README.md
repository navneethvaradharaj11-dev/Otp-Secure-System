# OTP Secure System

A Python-based One-Time Password (OTP) authentication system built to demonstrate authentication logic and practical version control using Git and GitHub.

---

## Project Overview

The **OTP Secure System** simulates a secure authentication workflow commonly used in modern login systems. It demonstrates core backend concepts such as OTP generation, expiration handling, limited verification attempts, and authentication flow design.

The application runs in the terminal and is designed for educational purposes to help understand how OTP-based authentication systems work internally.

---

## Features

* 6-digit OTP generation
* OTP expiration (60 seconds)
* Maximum of 3 verification attempts
* Mobile number validation
* OTP resend flow
* Terminal-based authentication workflow
* Modular Python project structure
* Integration with Twilio Verify API for OTP delivery

---

## Technologies Used

* **Python 3** – Programming language used to build the application
* **Twilio Verify API** – Service used to send and verify OTP messages
* **Git** – Version control system for tracking project changes
* **GitHub** – Repository hosting platform for collaboration and project management

---

## How to Run

### 1. Clone the repository

```id="p7u9od"
git clone https://github.com/navneethvaradharaj11-dev/otp-secure-system.git
```

### 2. Navigate to the project directory

```id="p8s2ja"
cd otp-secure-system
```

### 3. Install dependencies

```id="ybeu6h"
pip install -r requirements.txt
```

### 4. Configure Twilio credentials

Set the following environment variables:

```id="p4v2rb"
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_VERIFY_SERVICE_SID=your_verify_service_sid
```

### 5. Run the program

```id="8o4qyx"
python main.py
```

---

## Project Structure

```id="8te96a"
otp-secure-system/
│
├── main.py              # Application entry point
├── config.py            # Configuration settings and environment variables
├── otp_service.py       # OTP generation and verification logic
├── validators.py        # Mobile number validation
├── input_handler.py     # Timer and OTP input handling
├── twilio_service.py    # Twilio Verify API integration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Learning Objectives

This project was developed to practice:

* Python programming fundamentals
* Authentication system design concepts
* Time-based validation logic
* Implementing attempt limits for security
* Version control using Git
* Publishing and managing repositories using GitHub

---

## Disclaimer

This project is created for educational purposes.
OTP messages are sent using the Twilio Verify API and may be limited by Twilio trial account restrictions.

---

## Author

**Navneeth**

GitHub:
https://github.com/navneethvaradharaj11-dev
