"""Tests introspection and dynamic creation of conf_mgr."""
from random import random
from tempfile import TemporaryDirectory, mkstemp, mkdtemp

import pytest


@pytest.fixture()
def test_mock_project_configs(faker) -> TemporaryDirectory:
    """Return a Path to a generated directory tree, seeded with config files."""
    max_depth: int = 3
    named_file: str = "conf.py"
    named_probability: float = 0.75
    files: range = range(3)
    file_probability: float = 0.5
    sub_dirs: range = range(3)
    dir_probability: float = 0.5

    def populate_dir(current_dir: str, depth: int) -> None:
        depth += 1
        if random() <= named_probability:
            with open(f"{current_dir}/{named_file}", "x") as f:
                f.write(str(faker.pydict()))
        for file in files:
            if random() <= file_probability:
                mkstemp(dir=current_dir)
        if depth >= max_depth:
            return
        else:
            for sub_dir in sub_dirs:
                if random() <= dir_probability:
                    new_dir: str = mkdtemp(dir=current_dir)
                    populate_dir(new_dir, depth)
        return

    top_level_dir: TemporaryDirectory = TemporaryDirectory()
    populate_dir(top_level_dir.name, 0)

    return top_level_dir
