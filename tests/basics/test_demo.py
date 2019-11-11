def test_passes():
    """function is executed without error => test passes."""


def test_fails_assert():
    assert 0, "assertion fails => test fails"


def test_fails_exception():
    int("x")  # error anywhere => test fails"


def non_test_function():
    """This is not a test."""
