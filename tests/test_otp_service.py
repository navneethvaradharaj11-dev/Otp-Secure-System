from otp_service import generate_otp


def test_otp_length():
    otp = generate_otp()
    assert len(otp) == 6


def test_otp_digits_only():
    otp = generate_otp()
    assert otp.isdigit()
