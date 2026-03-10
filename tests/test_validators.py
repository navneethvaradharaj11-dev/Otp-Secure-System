from validators import is_valid_mobile_number


def test_valid_mobile_number():
    assert is_valid_mobile_number("9876543210")


def test_invalid_length():
    assert not is_valid_mobile_number("12345")


def test_invalid_start_digit():
    assert not is_valid_mobile_number("1234567890")
