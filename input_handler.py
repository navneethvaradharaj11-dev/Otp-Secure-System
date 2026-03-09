import os
import sys
import time

from config import OTP_LENGTH

if os.name == "nt":
    import msvcrt
else:
    import select
    import termios
    import tty


def input_otp_with_deadline(end_time):
    otp_text = ""
    last_remaining = -1

    old_settings = None
    if os.name != "nt":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            remaining = max(0, int(end_time - time.time() + 0.999))
            minutes = remaining // 60
            seconds = remaining % 60

            if remaining != last_remaining:
                print(f"\r{minutes:02d}:{seconds:02d} | Enter OTP: {otp_text}", end="", flush=True)
                last_remaining = remaining

            if time.time() >= end_time:
                print()
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
                    print()
                    return otp_text
                if key in ("\b", "\x08", "\x7f"):
                    otp_text = otp_text[:-1]
                elif key.isdigit() and len(otp_text) < OTP_LENGTH:
                    otp_text += key

            time.sleep(0.05)
    finally:
        if os.name != "nt" and old_settings is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
