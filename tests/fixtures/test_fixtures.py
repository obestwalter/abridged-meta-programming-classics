import pytest


@pytest.fixture  # think of this as registering a fixture function
def the_answer():
    return 42


def test_using_fixture_passes(the_answer):  # request fixture result via name
    assert the_answer == 42


def test_using_fixture_fails(the_answer):
    assert the_answer == 23, f"{the_answer} is not 23 :("
