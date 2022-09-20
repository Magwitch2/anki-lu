"""Sphinx configuration."""
project = "Anki for Luxembourgish"
author = "Terry Hanold"
copyright = "2022, Terry Hanold"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
