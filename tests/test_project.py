from .context import cml

import unittest


class ProjectTest(unittest.TestCase):
    """Test cases for cml.project."""

    def test_project(self):
        project = cml.Project(cml.utils.data_dir())
        self.assertEquals(project.path, cml.utils.data_dir())
        self.assertTrue(project.exists())
        self.assertFalse(project.is_initialized())


if __name__ == '__main__':
    unittest.main()
