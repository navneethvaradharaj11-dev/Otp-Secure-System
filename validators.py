import phonenumbers


def is_valid_mobile_number(phone: str) -> bool:
    """Validate if a phone number is a valid Indian mobile number.

    Accepts numbers in local Indian format or with +91.
    """
    try:
        parsed_number = phonenumbers.parse(phone, "IN")
        return (
            phonenumbers.is_valid_number(parsed_number)
            and phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
        )
    except phonenumbers.NumberParseException:
        return False


def format_phone_number(phone: str) -> str:
    """Format a valid Indian phone number to E.164 format."""
    parsed_number = phonenumbers.parse(phone, "IN")
    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
