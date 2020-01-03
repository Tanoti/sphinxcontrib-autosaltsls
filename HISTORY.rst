History
========

0.5.0 (2020-01-03)
--------------------

* Fixed `Issue #10 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/10>`_ and added :confval:`autosaltsls_indented_comments` for this
* Added new directives:

    * :confval:`hidden` (`Issue #4 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/4>`_)
    * :confval:`ignore` (`Issue #2 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/2>`_)
    * :confval:`environment` (`Issue #7 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/7>`_)
    * :confval:`topfile_id` (`Issue #7 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/7>`_)

* Detect and display sls file format if set using '#!' at the top of the file (`Issue #3 <https://github.com/Tanoti/sphinxcontrib-autosaltsls/issues/3>`_)

0.4.0 (2019-12-23)
--------------------

* Added support for source-specific Sphinx role/object types

0.3.0 (2019-12-20)
--------------------

* Added :confval:`autosaltsls_display_master_indices` to suppress indices on master index page

0.2.12 (2019-12-19)
--------------------

* Added :confval:`expand_title_name` to source settings for generating unique titles and added to example fileset config
* Tidied documentation

0.2.11 (2019-12-18)
--------------------

* Added :confval:`title_prefix` and :confval:`title_suffix` to source settings for generating unique titles

0.2.10 (2019-12-17)
--------------------

* Removed option to pass :confval:`autosaltsls_sources` as a string

0.2.9 (2019-12-13)
-------------------

* Use black as code formatting standard