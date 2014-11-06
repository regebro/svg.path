import unittest
import doctest


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocFileSuite('../../../../README.rst'))
    return tests
