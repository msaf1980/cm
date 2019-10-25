from .context import cml

import unittest


class DoxygenTest(unittest.TestCase):
    """Test cases for cml.doxygen."""

    def test_thoughts(self):
        parser = cml.DoxygenParser()
        self.assertEquals(parser.f(), 'hello world')


if __name__ == '__main__':
    unittest.main()
