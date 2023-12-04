# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

current_dir = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
project_dir = os.path.join(current_dir, "py_ocpi/")
# autoapi_dirs = [os.path.join(project_dir, 'modules/')]
sys.path.insert(0, os.path.abspath(current_dir))
sys.path.insert(0, os.path.abspath(project_dir))

from py_ocpi import __version__  # noqa

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Extrawest OCPI"
copyright = "2023, Extrawest"
author = "Extrawest"
release = f"{__version__}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib.httpdomain",
    "sphinx.ext.autodoc",
    "sphinxcontrib.autohttp.flask",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_copybutton",
]

autodoc_typehints = "description"

templates_path = ["_templates"]
exclude_patterns = []  # type: ignore

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
html_static_path = ["_static"]
html_css_files = []  # type: ignore
html_theme_options = {
    "nosidebar": "false",
    "sidebarwidth": 380,
}

source_suffix = ".rst"
pygments_style = "sphinx"
