"""
Does some basic tests on the generated project.

Almost completely taken from (you guys rock!):
https://github.com/pydanny/cookiecutter-django/blob/master/tests
"""

import os
import re

import pytest
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r'{{(\s?cookiecutter)[.](.*?)}}'
RE_OBJ = re.compile(PATTERN)


@pytest.fixture
def context():
    """Creates default prompt values."""
    return {
        'project_name': 'test_project',
        'project_verbose_name': 'Test Project',
        'project_domain': 'myapp.com',
        'organization': 'wemake.services',
        'docker': 'y',
    }


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, _subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def assert_variables_replaced(paths):
    """Method to check that all paths have correct substitutions."""
    for path in paths:
        if is_binary(path):
            continue

        with open(path, 'r') as f:
            contents = f.read()

        match = RE_OBJ.search(contents)
        msg = 'cookiecutter variable not replaced in {0} at {1}'

        # Assert that no match is found:
        assert match is None, msg.format(path, match.start())


def test_with_default_configuration(cookies, context):
    """Tests project structure with default prompt values."""
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context['project_name']
    assert result.project.isdir()


def test_variables_replaced(cookies, context):
    """Ensures that all variables are replaced inside project files."""
    result = cookies.bake(extra_context=context)
    paths = build_files_list(str(result.project))

    assert paths
    assert_variables_replaced(paths)


@pytest.mark.parametrize('prompt,entered_value', [
    ('project_name', 'myProject'),
    ('project_name', '43prject'),
    ('project_name', '_test'),
    ('project_name', 'test_'),
    ('project_name', '1_test'),
    ('project_name', 'test@'),
    ('project_name', '0123456'),
    ('project_domain', 'https://wemake.services'),
    ('project_domain', 'wemake.services?search=python'),
    ('project_domain', ''),
])
def test_validators_work(prompt, entered_value, cookies, context):
    """Ensures that project can not be created with invalid name."""
    context.update({prompt: entered_value})
    result = cookies.bake(extra_context=context)

    assert isinstance(result.exception, FailedHookException)
    assert result.exit_code == -1
