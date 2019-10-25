from .context import cml

import unittest


class CMakeTest(unittest.TestCase):
    """Test cases for cml.cmake."""

    def test_cmake(self):
        parser = cml.CMakeParser()
        self.assertEquals(parser.f(), 'hello world')


if __name__ == '__main__':
    unittest.main()
