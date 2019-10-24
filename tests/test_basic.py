from .context import cmake_parser

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_get_hmm(self):
        self.assertEqual('hmmm...', cmake_parser.get_hmm())

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == '__main__':
    unittest.main()
