test_module_attribute = "this should never be discovered as a test!"


def test_passes_in_a_folder():
    pass


def test_fails_in_a_folder():
    assert 0, "I failed in a folder :("
