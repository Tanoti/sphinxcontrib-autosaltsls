Configuration
===============

This extension has two types of configuration options - top-level ones that control how the extension itself works and
source-specific ones that control how the sls files in a given source location should be processed.

Configuration Options
----------------------
These options should be set in the Sphinx ``conf.py`` file in your documentation area.

Required
~~~~~~~~
.. confval:: autosaltsls_sources

        The source areas in the Salt master's fileset (e.g. states, pillar, etc) to be documented. This can be provided
        in one of two ways:

        1. As a list of paths if you want to accept all the default source settings:

            .. code-block:: python

                autosaltsls_sources = ['states', 'pillar']

        2.  As a dict of source location to its settings (see :ref:`Source Settings`):

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

Optional
~~~~~~~~
.. confval:: autosaltsls_build_root

    Default: ``.``

    Location where the generated .rst files will saved

.. confval:: autosaltsls_comment_ignore_prefix

    Default: ``#!``

    Character/string used to denote lines which should be ignored when parsing a document comment block.

.. confval:: autosaltsls_comment_prefix

    Default: ``#``

    Character/string used to denote the contents of a document comment block.

.. confval:: autosaltsls_display_master_indices

    Default: ``True``

    Generate the  ``genindex``, ``modindex`` and ``search`` indices on the master index page when
    :confval:`autosaltsls_write_index_page` is set.

.. confval:: autosaltsls_doc_prefix

    Default: ``###``

    String used to denote the start of a document comment block.

.. confval:: autosaltsls_indented_comments

    Default: ``False``

    Comment blocks can be indented. All line parsing and processing routines will remove leading spaces before
    the :confval:`autosaltsls_doc_prefix` or :confval:`autosaltsls_comment_prefix` characters.

.. confval:: autosaltsls_index_template_path

    Default: ``''``

    Location of an override ``master.rst_t`` file to be used when generating the top-level index file
    (See  :ref:`Templates`).

.. confval:: autosaltsls_remove_first_space

    Default: ``True``

    Remove the first space from a line within a comment block. This is to allow for the usual practice of putting a
    space after a comment character but where that space is not needed in the rendered output

.. confval:: autosaltsls_sources_root

    Default: ``..``

    The directory under which the ``autosaltsls_sources`` are located. If you place your Sphinx project alongside the
    sources then this can be omitted, otherwise provide the path (e.g. ``/srv/salt``).

.. confval:: autosaltsls_source_url_root

    Default: ``None``

    Root URL to the files under the sources dirs in a source control system such as git. This is used to generate the
    ``[Source]`` link in the pages. If not supplied the link is suppressed.

    .. code-block:: python

        autosaltsls_source_url_root = 'https://github.com/myuser/saltfiles'

.. confval:: autosaltsls_write_index_page

    Default: ``False``

    Generate a top-level ``index.rst`` file which has a toctree that references the source-level index files.

Source Settings
----------------
The way in which the .sls files under a source location are parsed can be controlled using the following settings when
:confval:`autosaltsls_sources` is supplied as a dict:

.. confval:: build_dir

    Default: ``<autosaltsls_build_root>/<source>``.

    Path to put the built .rst files.

.. confval:: cross_ref_role

    Default: ``sls``

    Sphinx role to use when creating cross-reference targets in documents. By default all sls files are referenced using
    the ``:sls:`` role but this can cause problems when two targets from different sources have the same name. For
    example, ``states/apache.sls`` and ``pillar/apache.sls`` would both have the cross reference ``:sls:`apache``` but
    only one would be rendered properly.

.. confval:: exclude

    Default: ``None``

    A list of paths relative to the source location to exclude from parsing. This can be useful where a sub-directory
    of states need to be documented as their own source and corresponding top-level index entry.

.. confval:: expand_title_name

    Default: ``False``

    Flag to expand the sls name in the document page title. For example ``apache/installed.sls`` would render as
    ``apache.installed`` rather than ``installed``.

.. confval:: prefix

    Default: ``''``

    Prefix to add to the base sls name when rendering rst file contents.

.. confval:: template_path

    Default: ``None``

    The location of the template files for this source (index.rst_t, main.rst_t, sls.rst_t, top.rst_t). This is deemed
    to be relative to the Sphinx config path unless provided as an absolute path. (See :ref:`Templates`).

.. confval:: title

    Default: ``<source key>``

    The title to use on the index.rst page.

.. confval:: title_prefix

    Default: ``''``

    Prefix to add to the document title. This may be needed to ensure title uniqueness when using extensions like
    ``confluencebuilder``.

.. confval:: title_suffix

    Default: ``''``

    Suffix to append to the document title. This may be needed to ensure title uniqueness when using extensions like
    ``confluencebuilder``.

.. confval:: url_root

    Default: ``None``

    URL location of the source code controlled files for this source. Can be supplied as a full url starting with
    ``http(s)`` or a path relative to :confval:`autosaltsls_source_url_root`.

Source Settings Example
~~~~~~~~~~~~~~~~~~~~~~~~
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
                # Use the expanded name in the document title
                'expand_title_name': True,
                # Append a suffix to the title
                'title_suffix': ' (states)',
            },
            # Parse the 'pillar' directory under autosaltsls_sources_root
            # and accept all other default settings
            'pillar': {},
            # Parse the 'reactor' directory under autosaltsls_sources_root
            'reactor': {
                # Replace the title with 'Reactors'
                'title': 'Reactors',
            },
            # Parse the 'states/roles' directory under autosaltsls_sources_root
            'states/roles': {
                # Replace the title with 'Roles'
                'title': 'Roles',
                # Point the source code control url root tote correct location
                # as it is really under 'states'
                'url_root': 'states/roles',
                # Set the build dir to be 'roles' so it ends up as a top-level
                # entry
                'build_dir': 'roles',
                # Prefix the sls names with 'roles.' as that is the state name
                # a user needs to pass to state.apply, etc
                'prefix': 'roles.',
            },
        }

For a more complete example, please view the `example` page.