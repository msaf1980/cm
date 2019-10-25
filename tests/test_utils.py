from .context import cml

import unittest


class UtilsTest(unittest.TestCase):
    """Test cases for cml.utils."""

    def test_thoughts(self):
        utils = cml.Utils()
        self.assertEquals(utils.f(), 'hello world')


if __name__ == '__main__':
    unittest.main()
