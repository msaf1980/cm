from .context import cmake_parser

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(cmake_parser.hmm())


if __name__ == '__main__':
    unittest.main()
