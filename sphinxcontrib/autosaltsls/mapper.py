"""
AutoSaltSLS mapper class
"""
import os
import pathlib

from jinja2 import Environment, FileSystemLoader
from sphinx.errors import ExtensionError
from sphinx.util import logging, status_iterator

# noinspection PyUnresolvedReferences
from sphinx.util.console import darkgreen, bold

from .objects import AutoSaltSLS

logger = logging.getLogger(__name__)


class AutoSaltSLSMapperSettings(object):
    """
    Class to hold the source-level settings for a AutoSaltSLSMapper object.
    """

    def __init__(self, app, source, settings):
        # Pull in some app settings first
        self.doc_prefix = app.config.autosaltsls_doc_prefix
        self.comment_prefix = app.config.autosaltsls_comment_prefix
        self.comment_ignore_prefix = app.config.autosaltsls_comment_ignore_prefix

        # Now use the source settings
        self.build_dir = settings.get("build_dir", None)
        self.cross_ref_role = settings.get("cross_ref_role", "sls")
        self.exclude = settings.get("exclude", [])
        self.expand_title_name = settings.get("expand_title_name", None)
        self.no_first_space = settings.get("no_first_space", True)
        self.prefix = settings.get("prefix", None)
        self.title = settings.get("title", source)
        self.title_prefix = settings.get("title_prefix", "")
        self.title_suffix = settings.get("title_suffix", "")

        # Do some extra processing for the url_root
        self.url_root = settings.get("url_root", None)

        if app.config.autosaltsls_source_url_root:
            if self.url_root is None:
                self.url_root = app.config.autosaltsls_source_url_root + "/" + source
            else:
                if not self.url_root.startswith("http"):
                    self.url_root = (
                        app.config.autosaltsls_source_url_root + "/" + self.url_root
                    )


class AutoSaltSLSMapper(object):
    """
    Mapper to read sls files from a source location and to generate the relevant .rst files.

    app
        Sphinx app instance

    source
        Source key (e.g. 'states')

    settings
        Source settings from conf.py for the specified key
    """

    def __init__(self, app, source, settings):
        self.app = app
        self.source = source.replace("/", os.path.sep)
        self.full_source = source
        self.settings = settings
        self.sls_objects = []

        self._sub_object_count = None

        # Parse some settings into attributes
        self.settings = AutoSaltSLSMapperSettings(app, source, settings)

        # Expand the source to a full dir
        if not os.path.isabs(self.source):
            self.full_source = os.path.normpath(
                os.path.join(
                    app.confdir, app.config.autosaltsls_sources_root, self.source,
                )
            )

        # Work out the build root location for this source
        build_root = app.config.autosaltsls_build_root
        if not os.path.isabs(build_root):
            build_root = os.path.normpath(
                os.path.join(app.confdir, app.config.autosaltsls_build_root)
            )

        self.build_root = os.path.normpath(
            os.path.join(
                build_root,
                self.settings.build_dir.replace("/", os.path.sep)
                if self.settings.build_dir
                else self.source,
            )
        )

        # Work out the jinja template dirs to use
        template_paths = [
            os.path.normpath(
                os.path.join(os.path.realpath(__file__), "..", "templates")
            )
        ]

        # Add source template path to list
        source_template_path = settings.get("template_path", None)
        if source_template_path:
            if not os.path.isabs(source_template_path):
                source_template_path = os.path.normpath(
                    os.path.join(app.confdir, source_template_path)
                )
            logger.debug(
                "[AutoSaltSLS] Adding template path '{0}'".format(source_template_path)
            )
            template_paths.insert(0, source_template_path)

        # Initialise the jinja rendering engine
        self.jinja_env = Environment(loader=FileSystemLoader(template_paths))

    def load(self):
        """
        Read the files associated with the sls objects and parse their comment blocks
        """
        # Process all the sls objects and their files
        for sls_obj in status_iterator(
            self.sls_objects,
            bold("[AutoSaltSLS] Reading primary sls... "),
            "darkgreen",
            self.sls_objects_count,
            self.app.verbosity,
            stringify_func=_stringify_sls,
        ):
            # Parse the sls object's file and add to the object as an entry
            sls_obj.parse_file()

            # Some debugging info
            if sls_obj.header.has_text:
                logger.debug(
                    "[AutoSaltSLS] {0} extracted header:\n{1}".format(
                        "Top File" if sls_obj.topfile else "File",
                        sls_obj.header.annotated_text,
                    )
                )

            if sls_obj.body:
                logger.debug(
                    "[AutoSaltSLS] {0} extracted body:\n{1}".format(
                        "Top File" if sls_obj.topfile else "File",
                        sls_obj.annotated_body,
                    )
                )

            # Now parse any files belong to its children
            for sls_child_obj in status_iterator(
                sls_obj.children,
                bold("[AutoSaltSLS] Reading child sls... "),
                "darkgreen",
                sls_obj.child_count,
                self.app.verbosity,
                stringify_func=_stringify_sls,
            ):
                sls_child_obj.parse_file()
                if sls_child_obj.text:
                    logger.debug(
                        "[AutoSaltSLS] Child extracted text:\n{0}".format(
                            sls_child_obj.text
                        )
                    )

    @property
    def other_files(self):
        """
        Return the list of sls objects not marked as top files

        :return: list
        """
        sls_objs = [x for x in self.sls_objects if not x.topfile]
        sls_objs.sort(key=lambda sls: sls.name)
        return sls_objs

    @property
    def sls_objects_count(self):
        """
        Return the count of sls objects

        :return: int
        """
        return len(self.sls_objects)

    @property
    def sls_sub_object_count(self):
        """
        Return the count of child objects belonging to the top-level sls objects

        :return: int
        """
        if self._sub_object_count is None:
            self._sub_object_count = 0

            for sls_obj in self.sls_objects:
                self._sub_object_count += sls_obj.child_count

        return self._sub_object_count

    def scan(self):
        """
        Scan the source dir for ``*.sls`` files and create an AutoSaltSLS object for each

        :return: int (count of sls objects found)
        """
        # Check the source dir exists
        if not os.path.isdir(self.full_source):
            raise ExtensionError(
                "Source path '{0}' does not exist".format(self.full_source)
            )

        logger.info(bold("[AutoSaltSLS] ") + "Scanning {0}".format(self.full_source))

        cwd = os.getcwd()
        os.chdir(self.full_source)

        # Clear out any old data
        self.sls_objects = []

        for dir_path, dir_names, filenames in os.walk("."):
            # logger.debug('JPH - {0}, {1}, {2}'.format(dir_path, dir_names, filenames))
            # Remove the source from the dir we are processing as this will give us the sls namespace
            p = pathlib.Path(dir_path)
            rel_path = dir_path
            if dir_path != ".":
                rel_path = str(pathlib.Path(*p.parts[:]))

            source_url_path = None

            if self.settings.url_root:
                source_url_path = (
                    self.settings.url_root + "/" + rel_path.replace("\\", "/")
                )

            # Skip any paths in the exclude list
            if rel_path in self.settings.exclude:
                logger.info(
                    bold("[AutoSaltSLS] ") + darkgreen("Ignoring {0}".format(dir_path))
                )
                dir_names[:] = []
                filenames[:] = []
                continue

            # Start with an empty parent
            sls_parent = None

            # Create a parent container object if not in the top level
            if rel_path != ".":
                logger.debug(
                    "[AutoSaltSLS] Creating sls object for {0} (No file)".format(
                        rel_path
                    )
                )
                sls_parent = AutoSaltSLS(
                    self.app,
                    rel_path,
                    self.full_source,
                    self.settings,
                    source_url_root=source_url_path,
                )
                self.sls_objects.append(sls_parent)

            for file in filenames:
                # We only want .sls files
                if file.endswith(".sls"):
                    # init.sls files are the parent so update the right object
                    if file == "init.sls" and sls_parent:
                        sls_parent.initfile = True
                        continue

                    # Create an sls object for the file
                    logger.debug(
                        "[AutoSaltSLS] Creating sls object for {0} ({1})".format(
                            rel_path if rel_path != "." else "[root]", file,
                        )
                    )
                    sls_obj = AutoSaltSLS(
                        self.app,
                        file,
                        os.path.join(self.full_source, rel_path)
                        if rel_path != "."
                        else self.full_source,
                        self.settings,
                        parent_name=sls_parent.name if sls_parent else None,
                        source_url_root=source_url_path,
                    )

                    if sls_parent:
                        # Add the child to the parent
                        sls_parent.add_child(sls_obj)
                    else:
                        self.sls_objects.append(sls_obj)

        # Post-process the sls objects to set the initfile data correctly for true parent objects and to identify any
        # top files
        for sls_obj in self.sls_objects:
            if sls_obj.initfile:
                logger.debug(
                    "[AutoSaltSLS] Setting sls object {0} as init file".format(
                        sls_obj.basename
                    )
                )

                rst_filename = None
                if not sls_obj.child_count:
                    rst_filename = sls_obj.basename.replace(".", os.sep) + ".rst"

                sls_obj.set_initfile(rst_filename=rst_filename)

        # Change back to the starting dir
        os.chdir(cwd)

        # Report the count of objects found
        logger.info(
            bold("[AutoSaltSLS] ")
            + "Found {0} top-level sls entities and {1} sub-entities".format(
                self.sls_objects_count, self.sls_sub_object_count,
            )
        )

        return self.sls_objects_count

    @property
    def top_files(self):
        """
        Return the list of sls objects marked as top files

        :return: list
        """
        return [x for x in self.sls_objects if x.topfile]

    def write(self):
        """
        Generate the rst files for the loaded sls objects
        """
        # Create the build dir for our source
        if not os.path.exists(self.build_root):
            logger.info(
                bold("[AutoSaltSLS] ")
                + "Creating '{0}' build root dir '{0}'".format(
                    self.source, self.build_root
                )
            )

            try:
                os.mkdir(self.build_root)
            except PermissionError:
                raise ExtensionError(
                    "Could not create '{0}, permission denied".format(self.build_root)
                )

        # Loop over the sls objects and write out their rst files
        for sls_obj in status_iterator(
            self.sls_objects,
            bold("[AutoSaltSLS] Generating rst files... "),
            "darkgreen",
            self.sls_objects_count,
            self.app.verbosity,
        ):
            sls_obj.write_rst_files(self.jinja_env, self.build_root)

        # Write out the source index file
        index_file = os.path.join(self.build_root, "index.rst")

        template_obj = self.jinja_env.get_template("index.rst_t")

        logger.info(
            bold("[AutoSaltSLS] ")
            + "Rendering index file '{0}' using '{1}'".format(
                index_file, template_obj.filename,
            )
        )

        # Render the template using Jinja
        with open(index_file, "w") as outfile:
            outfile.write(template_obj.render(obj=self))


#
# Private functions
#
def _stringify_sls(sls_obj):
    return "{0} ({1})".format(sls_obj.name, sls_obj.filename)
