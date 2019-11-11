import pytest

@pytest.mark.charlie                # marker name can be any valid identifier
def test_fails_marked_charlie():
    assert 0, "This is bad!"

@pytest.mark.lucy
def test_passes_marked_lucy():
    pass

@pytest.mark.lucy
@pytest.mark.charlie                # a test can be marked with several markers
def test_passes_marked_lucy_and_charlie():
    pass
