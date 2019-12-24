Comment Block Format
=====================

A document comment block is a contiguous set of commented lines which follow an arbitrary block start marker. It is
semantically divided into a Summary (all text to the first blank line) and Content (the rest) and is known as an 'entry'
by the parser.

A block is identified by the parsing engine when it detects the start prefix specified by ``autosaltsls_doc_prefix``
(default is '###'). Then all subsequent lines that start with the comment character specified by
``autosaltsls_comment_prefix`` (default is '#') are loaded as data. The block ends when the first non-comment line
or new block start string is read. Lines that begin with the ignore prefix specified in ``autosaltsls_comment_ignore_prefix``
(default is '#!') are not loaded.

The first document comment block in a file is denoted as being the Header and all other comment blocks are the Body. This
allows for the indexing routines to extract the header summaries, etc.

Any valid Sphinx formatting commands should be able to be used in a document comment block.

Directives
-----------
Within a file and its document comment blocks the parsing can be manipulated by directives. These follow the document
start prefix (multiple directives can be supplied by separating them with commas although this is not often needed).

.. confval:: topfile

    Scope: File

    Identifies the current sls file as a salt top file (See `Salt Top Files <https://docs.saltstack.com/en/latest/ref/states/top.html>`_).
    Files with the name ``top.sls`` are automatically identified so this is only needed for alternate top files that
    might be passed to ``state.top``.

.. confval:: include

    Scope: Entry

    Provided the line following this directive is ``include:`` then the entries for that YAML key will be read into a
    list of includes to be rendered as cross-ref links to other sls files if possible.

.. confval:: show_id

    Scope: Entry

    Read the first line following this comment block and add it as a content line.

.. confval:: summary_id

    Scope: Entry

    Read the first line following this comment block and add it as the entry summary.

.. confval:: step

    Scope: Entry

    This entry is to be added to the numbered list of steps

.. confval:: step_id

    Scope: Entry

    Read the first line following this comment block and add it as summary, then add the entry to the numbered list
    of steps

Cross-referencing SLS files
----------------------------
The AutoSaltSLS extension makes use of a custom Sphinx role ``sls`` to create cross-references between sls files. This
is how the :confval:`include` directive can build the list included files and have them link to their target. You can
use the default ``sls`` role or a source-specific role you have defined using :confval:`cross_ref_role` to insert your
own cross-references between sls files.

Configuration Example
----------------------
The following is a contrived comment block::

    ###
    # This line is the header summary
    #
    # Text following a blank line will be the content.
    # This will be rendered as a cross-reference - :sls:`targetsls`

    ###
    # Any subsequent comment blocks are the body with a summary...
    #
    # ... and content

    ### summary_id
    # This text will be the content after the summary which has been
    # generated using the first non-comment line following the comment
    # block.
    This-line-becomes-a-summary

    ### step
    # This line is the summary for a numbered step
    #
    # And this text will be the content

    ### step_id
    # This text will be the content after the summary which has been
    # generated using the first non-comment line following the comment
    # block. The entry is also rendered as a numbered step.
    This-line-becomes-a-step-summary
