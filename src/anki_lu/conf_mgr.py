"""Manages instantiation and validation of package config object.

This class handles access and management of data persistence (e.g. json files),
enabling the conf files to focus purely on defining the model
"""
from importlib import util
from inspect import getmembers
from pathlib import Path

from pydantic import BaseModel

def_file_name: str = "config.json"
def_module_name: str = "conf"
def_model_name: str = "Configuration"
_pkg_path: Path = Path(__file__).parent
_pkg_name: str = _pkg_path.stem


def get_config_obj(
    data: str = def_file_name,
    pkg_dir: Path = _pkg_path,
    module: str = def_module_name,
    model: str = def_model_name,
) -> BaseModel:
    """Accesses persistence (json), and uses it to instantiate config model.

    There are several requirements for current implementation to work:
    -   this module and conf module are both in top-level pkg directory,
    -   the conf data file is json format.

    Args:
        data: name of data file (only json support currently)
        pkg_dir: Path to top-level directory holding module and data file
        module: name of module defining config model (e.g. conf)
        model: name of class in conf module that sets data model

    Returns:
        A validated config model (based on pydantic BaseModel).

    Raises:
        FileNotFoundError: if conf module isn't found.
        NameError: if model (class) isn't found.
        ValueError: if json file data has validation error during instantiation.
    """
    #  Supports cases (e.g. test) when module is not in package folder.
    #  Recipe for direct import of source file: https://bityl.co/Elxf
    file_path: Path = pkg_dir.joinpath(module).with_suffix(".py")
    spec = util.spec_from_file_location(module, file_path)
    c_module = util.module_from_spec(spec)  # type: ignore[arg-type]
    try:
        spec.loader.exec_module(c_module)  # type: ignore[union-attr]
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"{exc}: run from <test>, {module} could not be imported"
        ) from exc

    c_model: BaseModel = BaseModel()
    for n, v in getmembers(c_module):
        if n == model:
            c_model = v
            break
    if c_model == BaseModel():
        raise NameError(f"{model} not found in {module}")

    # no tests written for try block, pydantic handles validation/errors
    try:  # pragma: no cover
        if pkg_dir == _pkg_name:  # pragma: no cover
            conf_obj = c_model.parse_file(data)  # pragma: no cover
        else:  # pragma: no cover
            conf_obj = c_model.parse_file(pkg_dir.joinpath(data))  # pragma: no cover
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"{exc}: issue with data format") from None  # pragma: no cover

    return conf_obj
