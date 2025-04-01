import os

from unittest import TestCase

from common.constants import get_env


class Test(TestCase):

    def test_get_env_no_file(self):
        # there is no file in that path
        default_value = "qwert"
        actual = get_env('PROJECT_NAME', '../../project_env/project_name.txt', default_value)

        self.assertEqual(actual, default_value)

    # @unittest.skip
    def test_get_env_with_file(self):
        # this test case depends on the file project_name.txt
        # so, it will fail if the file changes
        actual = get_env('PROJECT_NAME', '../../../project_env/sample/project_name.txt')

        self.assertEqual(actual, 'project_name')

    def test_get_local_env(self):
        # Set environment variable
        # given
        expect_env_value = 'value'
        os.environ['PROJECT_NAME'] = expect_env_value

        # when
        actual = get_env('PROJECT_NAME', "unnecessary")

        # then
        self.assertEqual(actual, expect_env_value)
