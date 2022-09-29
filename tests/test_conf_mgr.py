"""Tests conf_mgr."""

import shutil
from pathlib import Path
from tempfile import mkdtemp
from typing import Any

import pytest

from anki_lu import conf_mgr


@pytest.fixture()
def conf_dir_struct() -> dict:
    """Creates a mock package directory, seeded with conf and json files."""
    data: list = [
        ["string_key", "string_value with SPACES."],
        ["path_key", "/Users/terry/Desktop/Lëtzebuergesch.apkg"],
    ]
    data_file_name: str = "test_config.json"
    module_name: str = "test_conf"
    model_name: str = "TestConfiguration"
    pkg_path: str = mkdtemp(dir=Path(__file__).parent)
    with open(f"{pkg_path}/__init__.py", "x") as f:
        f.write("makes directory a package")
    with open(f"{pkg_path}/{data_file_name}", "x") as f:
        f.write("{")
        f.write(f'"{data[0][0]}": "{data[0][1]}", ')
        f.write(f'"{data[1][0]}": "{data[1][1]}"')
        f.write("}")
    with open(f"{pkg_path}/{module_name}.py", "x") as f:
        f.write("from pydantic import BaseModel\n")
        f.write("from pathlib import Path\n")
        f.write(f"class {model_name}(BaseModel):\n")
        f.write(f"    {data[0][0]}: str\n")
        f.write(f"    {data[1][0]}: Path\n")

    yield {
        "config_data": data,
        "data_path": data_file_name,
        "pkg_path": Path(pkg_path),
        "module_name": module_name,
        "model_name": model_name,
    }
    shutil.rmtree(pkg_path)


def test_get_config_obj(conf_dir_struct) -> None:
    """Tests happy path.

    GIVEN: valid package structure, data file, and conf module
    WHEN: config obj is generated
    THEN: each config key/value in data is in model
    """
    test_config = conf_mgr.get_config_obj(
        data=conf_dir_struct["data_path"],
        pkg_dir=Path(conf_dir_struct["pkg_path"]),
        module=conf_dir_struct["module_name"],
        model=conf_dir_struct["model_name"],
    )
    data: list[str, Any] = conf_dir_struct["config_data"]
    for k, v in data:
        try:
            if k.startswith("path"):
                v = Path(v)
            assert getattr(test_config, k) == v
        except KeyError as err:
            raise KeyError(f"{err}: key is not an attribute in model") from err


def test_get_config_with_bad_module(conf_dir_struct) -> None:
    """Tests missing/wrong module.

    GIVEN a flawed project structure, with missing conf module
    WHEN get_config is called
    THEN a NameError exception is raised
    """
    with pytest.raises(NameError) as excinfo:
        test_config = conf_mgr.get_config_obj(  # noqa: F841
            data=conf_dir_struct["data_path"],
            pkg_dir=Path(conf_dir_struct["pkg_path"]),
            module="doesnt_exist",
            model=conf_dir_struct["model_name"],
        )
    assert "not found" in str(excinfo.value)


def test_get_config_with_bad_class(conf_dir_struct) -> None:
    """Tests missing/wrong configuration class.

    GIVEN a flawed project structure, with mis-named config class
    WHEN get_config is called
    THEN a NameError exception is raised
    """
    with pytest.raises(NameError) as excinfo:
        test_config = conf_mgr.get_config_obj(  # noqa: F841
            data=conf_dir_struct["data_path"],
            pkg_dir=Path(conf_dir_struct["pkg_path"]),
            module=conf_dir_struct["module_name"],
            model="doesnt_exist",
        )
    assert "not found in" in str(excinfo.value)
