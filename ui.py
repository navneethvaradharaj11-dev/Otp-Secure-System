import os
import atexit

BOX_WIDTH = 55
INNER_WIDTH = BOX_WIDTH - 2
_last_rendered_lines = 0
_cursor_hidden = False


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def _hide_cursor():
    global _cursor_hidden
    if not _cursor_hidden:
        print("\x1b[?25l", end="", flush=True)
        _cursor_hidden = True


def _show_cursor():
    global _cursor_hidden
    if _cursor_hidden:
        print("\x1b[?25h", end="", flush=True)
        _cursor_hidden = False


def _line(content=""):
    text = content[:INNER_WIDTH].ljust(INNER_WIDTH)
    return f"|{text}|"


def _center(text=""):
    return _line(text.center(INNER_WIDTH))


def _otp_slots(otp_text, otp_length):
    chars = list(otp_text[:otp_length])
    chars.extend(["_"] * (otp_length - len(chars)))
    return " ".join(chars)


def _fit(text):
    return text[:INNER_WIDTH]


def _draw_panel(panel_text):
    global _last_rendered_lines
    line_count = panel_text.count("\n") + 1
    _hide_cursor()

    if _last_rendered_lines > 0:
        print(f"\x1b[{_last_rendered_lines}F", end="")
        print("\x1b[J", end="")
    else:
        clear_screen()
    print(panel_text, flush=True)
    _last_rendered_lines = line_count


def end_panel_render():
    global _last_rendered_lines
    _last_rendered_lines = 0
    _show_cursor()


def render_otp_panel(phone, otp_text, remaining_seconds, otp_length, helper_text="", status_text=""):
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    lines = [
        "+" + "-" * INNER_WIDTH + "+",
        _center("OTP Secure System"),
        _line("-" * INNER_WIDTH),
        _line(_fit(f" Mobile Number : {phone}")),
        _line(),
        _line(_fit(f" OTP Slot      : [{_otp_slots(otp_text, otp_length)}]")),
        _line(_fit(f" Time Left     : {minutes:02d}:{seconds:02d}")),
        _line(),
        _line(_fit(f" {helper_text or 'Enter OTP digits, then press Enter.'}")),
        _line(_fit(f" {status_text or 'Waiting for input...'}")),
        _line(),
        _center("Verify OTP"),
        "+" + "-" * INNER_WIDTH + "+",
    ]
    return "\n".join(lines)


def show_otp_panel(phone, otp_text, remaining_seconds, otp_length, helper_text="", status_text=""):
    panel = render_otp_panel(phone, otp_text, remaining_seconds, otp_length, helper_text, status_text)
    _draw_panel(panel)


def render_prompt_panel(phone, prompt_text, input_text="", status_text=""):
    lines = [
        "+" + "-" * INNER_WIDTH + "+",
        _center("OTP Secure System"),
        _line("-" * INNER_WIDTH),
        _line(_fit(f" Mobile Number : {phone}")),
        _line(),
        _line(" OTP Session"),
        _line(),
        _line(_fit(f" {prompt_text}")),
        _line(_fit(f" Input         : {input_text}")),
        _line(_fit(f" {status_text}")),
        _line(),
        _center("Verify OTP"),
        "+" + "-" * INNER_WIDTH + "+",
    ]
    return "\n".join(lines)


def show_prompt_panel(phone, prompt_text, input_text="", status_text=""):
    panel = render_prompt_panel(phone, prompt_text, input_text, status_text)
    _draw_panel(panel)


atexit.register(_show_cursor)
