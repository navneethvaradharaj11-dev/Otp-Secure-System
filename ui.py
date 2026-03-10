import os
import atexit

if os.name == "nt":
    os.system("")

BOX_WIDTH = 74
INNER_WIDTH = BOX_WIDTH - 2
_last_rendered_lines = 0
_cursor_hidden = False
RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
CYAN = "\x1b[36m"


def clear_screen() -> None:
    """Clear terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def _hide_cursor() -> None:
    global _cursor_hidden
    if not _cursor_hidden:
        print("\x1b[?25l", end="", flush=True)
        _cursor_hidden = True


def _show_cursor() -> None:
    global _cursor_hidden
    if _cursor_hidden:
        print("\x1b[?25h", end="", flush=True)
        _cursor_hidden = False


def _line(content: str = "", color: str = "") -> str:
    text = content[:INNER_WIDTH].ljust(INNER_WIDTH)
    if color:
        return f"|{color}{text}{RESET}|"
    return f"|{text}|"


def _center(text: str = "") -> str:
    return _line(text.center(INNER_WIDTH))


def _otp_slots(otp_text: str, otp_length: int) -> str:
    chars = list(otp_text[:otp_length])
    chars.extend(["_"] * (otp_length - len(chars)))
    return " ".join(chars)


def _fit(text: str) -> str:
    return text[:INNER_WIDTH]


def _status_color(status_text: str) -> str:
    lowered = status_text.lower()
    if any(word in lowered for word in ("incorrect", "invalid", "unable", "error", "expired", "locked", "missing")):
        return RED
    if any(word in lowered for word in ("successful", "verified", "approved")):
        return GREEN
    if status_text:
        return CYAN
    return ""


def _draw_panel(panel_text: str) -> None:
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


def end_panel_render() -> None:
    global _last_rendered_lines
    _last_rendered_lines = 0
    _show_cursor()


def render_otp_panel(
    phone: str,
    otp_text: str,
    remaining_seconds: int,
    otp_length: int,
    helper_text: str = "",
    status_text: str = "",
) -> str:
    """Build OTP input panel text."""
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
        _line(_fit(f" {status_text or 'Waiting for input...'}"), color=_status_color(status_text or "Waiting for input...")),
        _line(),
        _center("Verify OTP"),
        "+" + "-" * INNER_WIDTH + "+",
    ]
    return "\n".join(lines)


def show_otp_panel(
    phone: str,
    otp_text: str,
    remaining_seconds: int,
    otp_length: int,
    helper_text: str = "",
    status_text: str = "",
) -> None:
    """Render OTP input panel."""
    panel = render_otp_panel(phone, otp_text, remaining_seconds, otp_length, helper_text, status_text)
    _draw_panel(panel)


def render_prompt_panel(
    phone: str,
    prompt_text: str,
    input_text: str = "",
    status_text: str = "",
) -> str:
    """Build generic prompt panel text."""
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
        _line(_fit(f" {status_text}"), color=_status_color(status_text)),
        _line(),
        _center("Verify OTP"),
        "+" + "-" * INNER_WIDTH + "+",
    ]
    return "\n".join(lines)


def show_prompt_panel(
    phone: str,
    prompt_text: str,
    input_text: str = "",
    status_text: str = "",
) -> None:
    """Render generic prompt panel."""
    panel = render_prompt_panel(phone, prompt_text, input_text, status_text)
    _draw_panel(panel)


atexit.register(_show_cursor)
