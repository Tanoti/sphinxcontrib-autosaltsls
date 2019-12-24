"""
Classes to describe AutoSaltAPI sls files as objects.
"""
import os
import re

from sphinx.util import logging
from sphinx.errors import ExtensionError

# noinspection PyUnresolvedReferences
from sphinx.util.console import darkgreen, bold

logger = logging.getLogger(__name__)


class AutoSaltSLS(object):
    """
    Object representation of an sls file or directory.

    app
        Sphinx application instance

    basename
        sls filename or group name
        (e.g. 'ssl_enabled.sls' or 'apache')

    source_path
        Full path to the location of the expected sls file for this object

    source_settings
        AutoSaltSLSMapperSettings object for the source creating this instance

    parent_name : None
        Name of the parent group
        (e.g. for 'ssl_enabled.sls' this might be 'apache')

    source_url_root: None
        URL root to the source control viewable files location
    """

    def __init__(
        self,
        app,
        basename,
        source_path,
        source_settings,
        parent_name=None,
        source_url_root=None,
    ):
        self.app = app
        self.basename, self.filename = self._parse_name(basename)
        self.source_path = source_path
        self.parent_name = parent_name
        self.source_settings = source_settings
        self.source_url_root = source_url_root
        self.full_filename = None

        # Build the full filename
        if self.filename:
            self.full_filename = os.path.join(source_path, self.filename)

        # Initialise some properties
        self.topfile = True if self.filename == "top.sls" else False
        self.initfile = True if self.filename == "init.sls" else False
        self.children = []
        self.entries = []
        self.steps = []
        self.include = None
        self.source_url = None
        self.docname = None

        # Internal properties
        self._header_entry = None

        # Work out some related filenames
        if self.filename:
            self.rst_filename = self.filename.replace(".sls", ".rst")
            self.docname = self.filename.replace(".sls", "")
        else:
            self.rst_filename = self.basename + ".rst"

        if self.source_url_root and self.filename:
            self.source_url = self.source_url_root + "/" + self.filename

    def __str__(self):
        return self.name

    def add_child(self, child_obj):
        """
        Add a child AutoSaltSLS to this instance.

        child_obj
            An AutoSaltSLS instance
        """
        self.children.append(child_obj)

    def add_entry(self, entry):
        """
        Add an AutoSaltSLSEntry entry object to this instance. If the entry is a step append it to the list of
        steps instead.

        entry
            An AutoSaltSLSEntry instance
        """
        self.entries.append(entry)

        # Do some entry-specific processing
        if entry.include:
            self.include = entry
        elif entry.is_step:
            self.steps.append(entry)

    @property
    def annotated_body(self):
        """
        Return the debug annotated text output for all body entries with newline terminators.

        :return: str
        """
        return "\n".join([x.annotated_text for x in self.body])

    @property
    def child_count(self):
        """
        Return the number of children.

        :return: int
        """
        return len(self.children)

    @property
    def body(self):
        """
        Return the list of entries comprising the body (i.e. everything except the header).

        :return: list
        """
        if self.entries and len(self.entries) > 1:
            return self.entries[1:]
        return []

    @property
    def body_text(self):
        """
        Return all the text for the body entries as one string with newline terminators.

        :return: str
        """
        return "\n\n".join([x.text for x in self.body])

    @property
    def header(self):
        """
        Return the first entry in the list or a dummy entry if there is no content.

        :return: AutoSaltSLSEntry
        """
        if not self._header_entry:
            try:
                self._header_entry = self.entries[0]
            except IndexError:
                self._header_entry = AutoSaltSLSEntry()

        return self._header_entry

    @property
    def name(self):
        """
        Return the full dot-separated name of the sls object (e.g. apache.sls_configured).

        :return: str
        """
        if self.parent_name:
            return "{0}.{1}".format(self.parent_name, self.basename)

        return self.basename

    def output_rst(
        self, jinja_env, output_dir, filename=None, template=None,
    ):
        """
        Generate the base rst file for this sls object.

        jinja_env
            Jinja Environment object to use when rendering templates

        output_dir
            Full path to the location for this file

        filename : None
            Filename to use for rst file, defaults to rst_filename property

        template : None
            Template file to use. Defaults to 'top.rst_t' for a topfile or 'sls.rst_t' otherwise
        """
        if filename is None:
            filename = self.rst_filename

        output_file = os.path.join(output_dir, filename)

        # Get the Jinja template
        if not template:
            template = "top.rst_t" if self.topfile else "sls.rst_t"

        template_obj = jinja_env.get_template(template)

        logger.debug(
            "[AutoSaltSLS] Rendering file '{0}' for {1} using '{2}'".format(
                output_file, self.name, template_obj.filename,
            )
        )

        # Render the template using Jinja
        with open(output_file, "w") as outfile:
            outfile.write(template_obj.render(sls=self))

    def parse_file(self):
        """
        Read the associated sls file, create an AutoSaltSLSEntry object for any comment blocks found and add them as
        entries.
        """
        if self.full_filename:
            with open(self.full_filename) as sls_file:
                entry = None
                included = False

                # Read each line
                for line in sls_file:
                    # Skip lines starting with comment ignore prefix (e.g. '#!')
                    if line.startswith(self.source_settings.comment_ignore_prefix):
                        continue

                    # Remove the newline
                    line = line.strip("\n")

                    # Start a block and create an AutoSaltSLSEntry object when we get the doc prefix (e.g. '###')
                    if line.startswith(self.source_settings.doc_prefix):
                        # Finish any current entry and store it in case we have two concurrent blocks without
                        # any lines in between
                        if entry:
                            self.add_entry(entry)

                        # Start a new entry
                        entry = AutoSaltSLSEntry()

                        # Strip off the prefix
                        line = line.replace(self.source_settings.doc_prefix, "")

                        # Check for directive keywords, stripping spaces from the fields
                        if line and not line.isspace():
                            directives = [x.strip() for x in line.split(",")]

                            # Process directives
                            for directive in directives:
                                # 'topfile' is an sls directive
                                if directive == "topfile":
                                    logger.debug(
                                        "[AutoSaltSLS] Marking sls {0} as top file".format(
                                            self.basename
                                        )
                                    )
                                    self.topfile = True

                                # Everything else is for an entry
                                elif hasattr(entry, directive):
                                    setattr(entry, directive, True)
                        continue

                    # End the block
                    if entry and not line.startswith(
                        self.source_settings.comment_prefix
                    ):
                        # Capture the first line (YAML ID) as content
                        if entry.show_id or entry.summary_id or entry.step_id:
                            if line[-1] == ":":
                                line = line[:-1]

                            if entry.summary_id or entry.step_id:
                                # Prepend with a newline so the summary is correctly identified later
                                entry.prepend_line("")
                                entry.prepend_line(line)
                            else:
                                entry.append_line(line)

                        # Read all the include entries (flag set by directive above)
                        elif entry.include:
                            if "include:" in line:
                                included = True
                                continue
                            elif included and line and not line.isspace():
                                # Use regex to match an include entry and store it
                                # First non-match will trigger block end
                                match = re.search("^\s+-\s+([\w\-.]+)", line)
                                if match:
                                    text = match.group(1)

                                    if text.startswith("."):
                                        text = "{0} <{1}{2}>".format(
                                            text,
                                            self.parent_name
                                            if self.parent_name
                                            else self.name,
                                            text,
                                        )

                                    entry.add_include(text)
                                    continue

                        # Add the entry to the main list
                        self.add_entry(entry)
                        entry = None
                        continue

                    # Any other comment line within an active block is part of the entry
                    if entry and line.startswith(self.source_settings.comment_prefix):
                        line = line.replace(self.source_settings.comment_prefix, "")

                        if self.app.config.autosaltsls_remove_first_space:
                            line = line[1:]

                        entry.append_line(line)

            # Catch there being no content after the comment document
            if entry:
                self.add_entry(entry)

    @property
    def prefixed_name(self):
        """
        Return the full dot-separated name of the sls object (e.g. apache.sls_configured) with the source-specific
        prefix applied.

        :return: str
        """
        if self.source_settings.prefix:
            return self.source_settings.prefix + self.name

        return self.name

    def set_initfile(self, rst_filename=None):
        """
        Shortcut function to set all the attributes needed for this object to be an init file.
        """
        self.filename = "init.sls"
        self.rst_filename = rst_filename if rst_filename else "init.rst"

        self.full_filename = os.path.join(
            self.source_path, self.basename.replace(".", os.sep), self.filename,
        )
        self.initfile = True

        if self.source_url_root:
            self.source_url = self.source_url_root + "/" + self.filename

    @property
    def text(self):
        """
        Return all the entries including the header as a string with newline terminators.

        :return: str
        """
        if self.entries:
            return "\n\n".join([x.text for x in self.entries])

        return ""

    @property
    def title(self):
        if self.topfile:
            title = self.filename
        elif self.source_settings.expand_title_name:
            title = self.name
        else:
            title = self.basename

        if self.source_settings.title_suffix or self.source_settings.title_prefix:
            title = "{0}{1}{2}".format(
                self.source_settings.title_prefix,
                title,
                self.source_settings.title_suffix,
            )

        return title

    @property
    def toc_entry(self):
        """
        Return the ``toctree`` entry for the top-level index file to use.

        :return: str
        """
        toc_entry = self.basename.replace(".", "/")

        if self.children:
            toc_entry = "{0}/{1}".format(toc_entry, "main")

        return toc_entry

    def write_rst_files(
        self, jinja_env, build_root_dir,
    ):
        """
        Write the rst files for this object and all children.

        jinja_env
            Jinja Environment object to use when rendering templates

        build_root_dir
            Root dir for the source output files

        :return: int
            Count of files created
        """
        file_count = 0

        if self.children:
            # Create the parent dir
            output_dir = os.path.join(
                build_root_dir, self.basename.replace(".", os.path.sep)
            )

            if not os.path.exists(output_dir):
                logger.debug(
                    "[AutoSaltSLS] Creating build dir '{0}'".format(output_dir)
                )

                try:
                    os.mkdir(output_dir)
                except PermissionError:
                    raise ExtensionError(
                        "Could not create '{0}', permission denied".format(output_dir)
                    )

            # Generate the main index
            self.output_rst(
                jinja_env, output_dir, filename="main.rst", template="main.rst_t"
            )
            file_count += 1

            # Write out our init base file
            if self.initfile:
                self.output_rst(jinja_env, output_dir)

            # Generate the base files for the children
            for sls_obj in self.children:
                sls_obj.output_rst(jinja_env, output_dir)
                file_count += 1
        else:
            self.output_rst(jinja_env, build_root_dir)
            file_count += 1

        return file_count

    #
    # Private functions
    #
    @staticmethod
    def _parse_name(basename):
        # Replace the path separator with a dot
        basename = basename.replace(os.path.sep, ".")

        if basename.endswith(".sls"):
            return basename.replace(".sls", ""), basename

        return basename, ""


class AutoSaltSLSEntry(object):
    """
    Object representation of an sls file comment block. The data is logically split into a summary (all text to the
    first blank line) and content (the rest).

    text : None
        Initial text to place in ``lines``

    **Directives**

        Directives are run-time changes to apply to an entry. They are specified on the document prefix line as a
        comma-separated list

        include
            The lines following this comment block will be an ``include:`` section and should be parsed to add the YAML
            list data items to the ``includes`` list

        show_id
             Read the first line following this comment block and add it as a content line

        step
            This comment block entry is to be added to the numbered list of steps

        step_id
            Read the first line following this comment block and add it as summary then add the entry to the numbered
            list of steps

        summary_id
             Read the first line following this comment block and add it as the entry summary
    """

    def __init__(self, text=None):
        self.lines = []
        self.includes = []

        # Directives
        self.include = False
        self.show_id = False
        self.step = False
        self.step_id = False
        self.summary_id = False

        # Internal properties
        self._summary = None
        self._content = None

        # Initialise with any text we've been given
        if text is not None:
            self.lines = text.splitlines()

    def __str__(self):
        return self.text

    def add_include(self, include):
        """
        Add an include statement to the list.

        include
            Include statement to add
        """
        self.includes.append(include)

    @property
    def annotated_text(self):
        """
        Return an annotated output of the entry for inclusion in the sphinx debug output.

        :return: str
        """
        output = "========================================\n"
        output += "Summary:\n"
        output += self.summary + "\n"
        output += "========================================\n"

        if self.content:
            output += "Content:\n"
            output += self.content + "\n"
            output += "========================================\n"

        return output

    def append_line(self, text):
        """
        Append some text to the content lines.

        text
            Text to append to the content lines
        """
        self.lines.append(text)

        # Reset the internal content property
        self._content = None

    @property
    def content(self):
        """
        Return the content (i.e. everything after the first paragraph).

        :return: str
        """
        if self._content is None:
            self._split_lines()

        return self._content

    @property
    def has_text(self):
        """
        Return flag to say if the entry has any text stored.

        :return: bool
        """
        return True if self.lines else False

    @property
    def is_step(self):
        """
        Return whether the entry is a step or not.

        :return: bool
        """
        return self.step or self.step_id

    def prepend_line(self, text):
        """
        Add some text to the start of the content line list.

        text
            Text to add to the start of the content lines
        """
        self.lines.insert(0, text)

        # Reset the internal content property
        self._content = None

    @property
    def summary(self):
        """
        Return the first paragraph (i.e. down to the first blank line) of the content lines as the summary.

        :return: str
        """
        if self._summary is None:
            self._split_lines()

        return self._summary

    @property
    def text(self):
        """
        Return all the stored lines as a string joined with newline terminators.

        :return: str
        """
        return "\n".join(self.lines)

    #
    # Private Functions
    #
    def _split_lines(self):
        """
        Split the content lines list into a summary (text to first blank line) and body (the rest).
        """
        summary = []
        content = []

        # Reset the summary so we can use it as a flag
        self._summary = None

        if self.lines:
            self._content = ""

            for line in self.lines:
                if self._summary is None:
                    # Got the first blank line
                    if line == "" or line.isspace():
                        self._summary = "\n".join(summary)
                        continue
                    summary.append(line)
                else:
                    content.append(line)

            if summary and self._summary is None:
                self._summary = "\n".join(summary)

            if content:
                self._content = "\n".join(content)
        else:
            self._summary = ""
            self._content = ""
