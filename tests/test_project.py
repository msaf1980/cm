from .context import cml

import unittest


class ProjectTest(unittest.TestCase):
    """Test cases for cml.project."""

    def test_thoughts(self):
        project = cml.Project()
        self.assertEquals(project.f(), 'hello world')


if __name__ == '__main__':
    unittest.main()
