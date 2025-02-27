import doctest


def test_readme() -> None:
    doctest.testfile("../README.rst")
