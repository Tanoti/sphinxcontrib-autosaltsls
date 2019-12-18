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
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = 'Sphinx AutoSaltSLS Example'
copyright = '2019, John Hicks'
author = 'John Hicks'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.autosaltsls',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

#
# AutoSaltSLS
#
autosaltsls_sources = {
    'states': {
        'title': 'States',
        'exclude': [
            'roles',
        ],
        'template_path': '_templates/states',
        'title_suffix': ' (state)'
    },
    'pillar': {
        'title': 'Pillar',
        'title_suffix': ' (pillar)'
    },
    'reactor': {
        'title': 'Reactors',
    },
    'states/roles': {
        'title': 'Roles',
        'url_root': 'states/roles',
        'build_dir': 'roles',
        'prefix': 'roles.',
        'title_prefix': 'Roles-',
    },
}

autosaltsls_write_index_page = True
autosaltsls_index_template_path = '_templates'
