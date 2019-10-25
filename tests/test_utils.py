from .context import cml

import unittest


class UtilsTest(unittest.TestCase):
    """Test cases for cml.utils."""

    def test_utils(self):
        self.assertIsNotNone(cml.utils.script_dir())
        self.assertIsNotNone(cml.utils.data_dir())


if __name__ == '__main__':
    unittest.main()
