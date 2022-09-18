# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# Add document
import os
import sys
#sys.path.insert(0, os.path.abspath('.'))
#sys.path.insert(0, os.path.join(os.path.abspath('..'), "booklet"))
sys.path.insert(0, os.path.abspath('..'))
from pathlib import Path


news_path = Path("../NEWS")
news_document_path = Path("./develop/news.rst")

with open(news_path, "r") as source:
    source_string = source.readlines()
with open(news_document_path, "w") as doc:
    doc.writelines(["==========\n", "News\n","==========\n"])
    for st in source_string:
        doc.write(st)



from booklet.meta import __version__ as release_str



# -- Project information -----------------------------------------------------

project = 'HornPenguin Booklet'
copyright = '2022, Hyun Seong Kim'
author = 'Hyun Seong Kim'

# The full version, including alpha/beta/rc tags
release = release_str



# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinxawesome_theme'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'sphinx_rtd_theme'

html_permalinks_icon = '<span>#</span>'
html_theme = 'sphinxawesome_theme'
html_favicon = 'HornPavicon.ico'

html_theme_options = {
    "extra_header_links" : {"Docs": "docs", "홈":"publisher"}

}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


