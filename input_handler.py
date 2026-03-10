import os
import sys
import time
from typing import Optional

from config import OTP_LENGTH
from ui import show_otp_panel, show_prompt_panel

if os.name == "nt":
    import msvcrt
else:
    import select
    import termios
    import tty


def input_otp_with_deadline(end_time: float, phone: str, status_text: str) -> Optional[str]:
    """Capture OTP input until Enter or until the deadline expires."""
    otp_text = ""
    last_remaining = -1
    last_otp_text = None

    old_settings = None
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            remaining = max(0, int(end_time - time.time() + 0.999))

            if remaining != last_remaining or otp_text != last_otp_text:
                show_otp_panel(
                    phone,
                    otp_text,
                    remaining,
                    OTP_LENGTH,
                    helper_text="Enter OTP digits, then press Enter.",
                    status_text=status_text,
                )
                last_remaining = remaining
                last_otp_text = otp_text

            if time.time() >= end_time:
                return None

            key = None
            if os.name == "nt":
                if msvcrt.kbhit():
                    key = msvcrt.getwch()
            else:
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                if readable:
                    key = sys.stdin.read(1)

            if key is not None:
                if key in ("\r", "\n"):
                    return otp_text
                if key in ("\b", "\x08", "\x7f"):
                    otp_text = otp_text[:-1]
                elif key.isdigit() and len(otp_text) < OTP_LENGTH:
                    otp_text += key

            time.sleep(0.05)
    finally:
        if os.name != "nt" and old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)


def input_yes_no_with_panel(
    phone: str,
    prompt_text: str,
    status_text: str = "Type yes or no, then press Enter.",
) -> str:
    """Capture a yes/no style text input from the boxed terminal panel."""
    typed = ""
    last_typed = None

    old_settings = None
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            if typed != last_typed:
                show_prompt_panel(phone, prompt_text, typed, status_text)
                last_typed = typed

            key = None
            if os.name == "nt":
                if msvcrt.kbhit():
                    key = msvcrt.getwch()
            else:
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                if readable:
                    key = sys.stdin.read(1)

            if key is not None:
                if key in ("\r", "\n"):
                    return typed.strip().lower()
                if key in ("\b", "\x08", "\x7f"):
                    typed = typed[:-1]
                elif key.isalpha() and len(typed) < 3:
                    typed += key.lower()

            time.sleep(0.05)
    finally:
        if os.name != "nt" and old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)


def input_mobile_with_panel(
    prompt_text: str = "Enter mobile number:",
    status_text: str = "",
) -> str:
    """Capture mobile input from the boxed terminal panel."""
    typed = ""
    last_typed = None

    old_settings = None
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            current_status = status_text or "Enter a 10-digit number starting with 6/7/8/9."
            if typed:
                current_status = f"Digits entered: {len(typed)}/10"

            if typed != last_typed:
                show_prompt_panel("Not set", prompt_text, typed, current_status)
                last_typed = typed

            key = None
            if os.name == "nt":
                if msvcrt.kbhit():
                    key = msvcrt.getwch()
            else:
                readable, _, _ = select.select([sys.stdin], [], [], 0)
                if readable:
                    key = sys.stdin.read(1)

            if key is not None:
                if key in ("\r", "\n"):
                    return typed.strip()
                if key in ("\b", "\x08", "\x7f"):
                    typed = typed[:-1]
                elif key.isdigit() and len(typed) < 10:
                    typed += key

            time.sleep(0.05)
    finally:
        if os.name != "nt" and old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
