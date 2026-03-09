def is_valid_mobile_number(phone):
    if not (phone.isdigit() and len(phone) == 10):
        return False
    if phone[0] not in ["6", "7", "8", "9"]:
        return False
    if phone in {"1234567890", "0000000000"}:
        return False
    if phone == phone[0] * 10:
        return False
    return True
