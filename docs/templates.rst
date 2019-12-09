Templates
==========
Custom jinja templates can be specified for the master index file generated when :confval:`autosaltsls_write_index_page`
is enabled and for the files used when generating the documentation for a source.

Master Index Template
----------------------
When :confval:`autosaltsls_write_index_page` is enabled, the AutoSaltSLS extension will look in
:confval:`autosaltsls_index_template_path` for a jinja template file called ``master.rst_t``.

Source Templates
-----------------
For any given source configured in :confval:`autosaltsls_sources` the AutoSaltSLS extension will look for the following
template files in the location specified by the ``template_path`` setting for that source.

For example::

    autosaltsls_sources = {
        'states': {
            'title': 'States',
            'template_path': '_templates/states',
        },
    }


index.rst_t
^^^^^^^^^^^^
The source-level ``index.rst`` file is generated from this template. It will list any Top Files found in the source
location and other files as Entries.

top.rst_t
^^^^^^^^^^
The ``top.rst`` for a Top File (either ``top.sls`` or a file identified using the :confval:`topfile` directive) is
rendered using this template.

main.rst_t
^^^^^^^^^^^
If a source contains a directory in which are sls files, the directory sls object's ``main.rst`` file is rendered using
this template. If the directory contains and ``init.sls`` file, that is displays here as the main entry contents and
any other sls files in the directory are listed as Elements.

sls.rst_t
^^^^^^^^^^
Any non-Top sls file's ``sls.rst`` file is rendered using this template. It displays the header entry and any sub-
entries.


