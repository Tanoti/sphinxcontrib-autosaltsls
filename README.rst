Sphinx AutoSaltSLS
*******************

Sphinx AutoSaltSLS provides  a way to automatically document Salt .sls files (e.g. states, pillar, reactors, etc) using
simple directives in the comments blocks of those files.

A comment block is identified using a block start string (default is ``###`) and contains all subsequent lines that start
with a given comment character (default is ``#``). The block ends when a new start string or a non-comment line is read.
Directives can be given in the comment block to control how the lines are parsed (see `Comment Block Format`).

Getting Started
================

The following steps will walk through how to add AutoSaltSLS to an existing Sphinx project. For instructions on how to
set up a Sphinx project, see Sphinx's documentation on `Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.

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
            'exclude': [
                'roles',
            ],
            'template_path': '_templates/autosaltsls/states',
        },
        'pillar' : {
            'title': 'Pillar'
        },
    }

The documentation will be built into the location specified by ``autosaltsls_build_root`` (defaults to '.')

Configuration Options
======================

.. confval:: autosaltsls_sources

        **Required**

        The source areas in the Salt master's fileset (e.g. states, pillar, etc) to be documented. This can be provided
        in one of three ways:

        1. As a single string if all files beneath a location are to be parsed:

            .. code-block:: python

                autosaltsls_sources = '/srv/salt'

        2. As a list of paths if you want to accept all the default source settings (see `Source Settings`):

            .. code-block:: python

                autosaltsls_sources = ['states', 'pillar']

        3.  As a dict of source location to its settings:

            .. code-block:: python

                autosaltsls_sources = {
                    'states': {
                        'title': 'States',
                        'exclude': [
                            'roles',
                        ],
                        'template_path': '_templates/autosaltsls/states',
                    },
                    'pillar' : {
                        'title': 'Pillar'
                    },
                }

.. confval:: autosaltsls_sources_root

    Default: ``..``

    The directory under which the ``autosaltsls_sources`` are located. If you place your Sphinx project alongside the
    sources then this can be omitted, otherwise provide the path (e.g. ``/srv/salt``).

.. confval:: autosaltsls_build_root

    Default: ``.``

    Location where the generated .rst files will saved

.. confval:: autosaltsls_doc_prefix

    Default: ``###``

    String used to denote the start of a document comment block.

.. confval:: autosaltsls_comment_prefix

    Default: ``#``

    Character/string used to denote the contents of a document comment block.

.. confval:: autosaltsls_comment_ignore_prefix

    Character/string used to denote lines which should be ignored when parsing a document comment block.

.. confval:: autosaltsls_remove_first_space

    Default: ``True``

    Remove the first space from a line within a comment block. This is to allow for the usual practice of putting a
    space after a comment character but where that space is not needed in the rendered output

.. confval:: autosaltsls_source_url_root

    Default: ``None``

    Root URL to the files under the sources dirs in a source control system such as git. This is used to generate the
    ``[Source]`` link in the pages. If not supplied the link is suppressed.

    .. code-block:: python

        autosaltsls_source_url_root = 'https://github.com/myuser/saltfiles'

Source Settings
================
The way in which the .sls files under a source location are parsed can be controlled using the following settings when
`autosaltsls_sources` is supplied as a dict:

.. confval:: title

    The title to use on the index.rst page, defaults to the source key.

.. confval:: exclude

    A list of paths relative to the source location to exclude from parsing. This can be useful where a sub-directory
    of states need to be documented as their own source and corresponding top-level index entry.

.. confval:: template_path

    The location of the template files for this source (index.rst_t, main.rst_t, sls.rst_t, top.rst_t). This is deemed
    to be relative to the Sphinx config path unless provided as an absolute path.

.. confval:: build_dir

    Path to put the built .rst files in, defaults to ``<autosaltsls_build_root>/<source>``.

.. confval:: prefix

    Prefix to add to the base sls name when rendering rst file contents.

Example
--------
The following is a commented example of a source dict:

.. code-block:: python

        autosaltsls_sources = {
            # Parse the 'states' directory under autosaltsls_sources_root
            'states': {
                # Replace the title with 'States'
                'title': 'States',
                # Exclude 'states/roles' from processing
                'exclude': [
                    'roles',
                ],
                # Use the templates in this dir in place of the standard ones
                'template_path': '_templates/autosaltsls/states',
            },
            # Parse the 'pillar' directory under autosaltsls_sources_root and accept all other default settings
            'pillar': {},
            # Parse the 'reactor' directory under autosaltsls_sources_root
            'reactor': {
                # Replace the title with 'Reactors'
                'title': 'Reactors',
            },
            # Parse the 'states/roles' directory under autosaltsls_sources_root
            'states/roles': {
                # Replace the title with 'Rolos'
                'title': 'Roles',
                # Point the source code control url root tote correct location as it is really under 'states'
                'url_root': 'states/roles',
                # Set the build dir to be 'roles' so it ends up as a top-level entry
                'build_dir': 'roles',
                # Prefix the sls names with 'roles.' as that is the state name a user needs to pass to state.apply, etc
                'prefix': 'roles.',
            },
        }

Comment Block Format
=====================

A comment block is a contiguous set of commented lines which follow a block start marker. It is semantically divided
into a Summary (all text to the first blank line) and Content (the rest).

A block is detected by the parsing engine when it detects the start string specified by ``autosaltsls_doc_prefix``
(default is '###') and then all subsequent lines that start with the comment character specified by
``autosaltsls_comment_prefix`` (default is '#') are loaded as data. The block ends when the first non-comment line
or new block start string is read.