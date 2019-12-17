Sphinx AutoSaltSLS
*******************

.. image:: https://img.shields.io/pypi/v/sphinxcontrib-autosaltsls.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-autosaltsls

.. image:: https://travis-ci.com/Tanoti/sphinxcontrib-autosaltsls.svg?branch=master
    :target: https://travis-ci.com/Tanoti/sphinxcontrib-autosaltsls

.. image:: https://readthedocs.org/projects/sphinxcontrib-autosaltsls/badge/?version=latest
    :target: https://sphinxcontrib-autosaltsls.readthedocs.io/en/latest/readme.html?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/Tanoti/sphinxcontrib-autosaltsls/shield.svg
    :target: https://pyup.io/repos/github/Tanoti/sphinxcontrib-autosaltsls/
    :alt: Updates

.. image:: https://pyup.io/repos/github/Tanoti/sphinxcontrib-autosaltsls/python-3-shield.svg
    :target: https://pyup.io/repos/github/Tanoti/sphinxcontrib-autosaltsls/
    :alt: Python 3

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Sphinx AutoSaltSLS provides a way to automatically document Salt .sls files (e.g. states, pillar, reactors, etc) using
simple directives in the comments blocks of those files.

A comment block is identified using a block start string (default is '###') and contains all subsequent lines that start
with a given comment character (default is '#''). The block ends when a new start string or a non-comment line is read.
Directives can be given in the comment block to control how the lines are parsed.

Getting Started
================

The following steps will walk through how to add AutoSaltSLS to an existing Sphinx project. For instructions on how to
set up a Sphinx project, see Sphinx's documentation on
`Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.

Installation
-------------

AutoSaltSLS can be installed through pip:

.. code-block:: bash

    pip install sphinxcontrib-autosaltsls

Next, add and configure AutoSaltSLS in your Sphinx project's ``conf.py``.

.. code-block:: python

    extensions.append('sphinxcontrib-autosaltsls')

    autosaltsls_sources = {
        'states': {
            'title': 'States',
            'template_path': '_templates/autosaltsls/states',
        },
        'pillar' : {
            'title': 'Pillar'
        },
    }

The documentation will be built into the location specified by ``autosaltsls_build_root`` (defaults to '.')

To configure AutoAPI behaviour further, see the
`Configuration documentation <https://sphinxcontrib-autosaltsls.readthedocs.io/en/latest/configuration.html>`_.

Basic Setup
------------
The absolute minimum setup is to set ``autosaltsls_sources`` as a list of directories under your salt fileset area (e.g.
``/srv/salt``) and let the extension index the files it finds. Documentation pages will be created but, unless the sls
files have had their document comment blocks enabled, they will say "No content".

.. code-block:: python

    autosaltsls_sources = [
        'states',
        'pillar',
    ]

See `Comment Block Format <https://sphinxcontrib-autosaltsls.readthedocs.io/en/latest/document.html>`_ for more
information on how to enable these.

To Do
======
* Write proper tests

Credits
========
This project was based on the logic behind both `readthedocs/sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_
and `Jakski/sphinxcontrib-autoyaml <https://github.com/Jakski/sphinxcontrib-autoyaml>`_, so many thanks to those projects
for getting me started.