"""
Sphinx Auto-SaltSLS top-level extension
"""
import os

from jinja2 import Environment, FileSystemLoader
from sphinx.errors import ExtensionError
from sphinx.util import logging

# noinspection PyUnresolvedReferences
from sphinx.util.console import darkgreen, bold

from .mapper import AutoSaltSLSMapper

__author__ = """John Hicks"""
__email__ = "johnhicks@fico.com"
__version__ = "0.4.2"

SETTINGS_STRING = [
    "build_dir",
    "cross_ref_role",
    "prefix",
    "template_path",
    "title",
    "title_prefix",
    "title_suffix",
    "url_root",
]

logger = logging.getLogger(__name__)


def run_autosaltsls(app):
    """
    Load AutoSaltSLS data from the filesystem
    """
    logger.debug("[AutoSaltSLS] Starting")

    if not app.config.autosaltsls_sources:
        raise ExtensionError("No autosaltsls_sources setting found in config")

    sources = {}

    # Convert str or list into dict
    if isinstance(app.config.autosaltsls_sources, dict):
        sources = app.config.autosaltsls_sources
    elif isinstance(app.config.autosaltsls_sources, list):
        for source in app.config.autosaltsls_sources:
            sources[source] = {}

    # Check the config options
    for source, settings in sources.items():
        if not isinstance(settings, dict):
            raise ExtensionError(
                "Settings for '{0}' in autosaltsls_sources must be a dict".format(
                    source,
                )
            )

        if "exclude" in settings and not isinstance(settings["exclude"], list):
            raise ExtensionError(
                "Entry 'exclude' for '{0}' in autosaltsls_sources setting must be a list".format(
                    source,
                )
            )

        if "expand_title_name" in settings and not isinstance(
            settings["expand_title_name"], bool
        ):
            raise ExtensionError(
                "Entry 'expand_title_name' for '{0}' in autosaltsls_sources setting must be a bool".format(
                    source,
                )
            )

        # Check the str type settings
        for key in SETTINGS_STRING:
            if key in settings and not isinstance(settings[key], str):
                raise ExtensionError(
                    "Entry '{0}' for '{1}' in autosaltsls_sources setting must be a string".format(
                        key, source,
                    )
                )

    # Check some other values
    if not isinstance(app.config.autosaltsls_write_index_page, bool):
        raise ExtensionError(
            "Config value 'autosaltsls_write_index_page' must be True or False only"
        )

    if not isinstance(app.config.autosaltsls_index_template_path, str):
        raise ExtensionError(
            "Config value 'autosaltsls_index_template_path' must be a string"
        )

    # Loop over the sources and do the work
    for source, settings in sources.items():
        # Create the mapper object
        sphinx_mapper = AutoSaltSLSMapper(app, source, settings)

        # Scan the files in the source to build an object list
        sphinx_mapper.scan()

        # Load the sls file contents into their respective objects
        sphinx_mapper.load()

        # Write the rst files in the correct order
        sphinx_mapper.write()

    # Write the master index
    if app.config.autosaltsls_write_index_page:
        # Work out the jinja template dirs to use
        template_paths = [
            os.path.normpath(
                os.path.join(os.path.realpath(__file__), "..", "templates")
            )
        ]

        index_template_path = app.config.autosaltsls_index_template_path
        if index_template_path:
            if not os.path.isabs(index_template_path):
                index_template_path = os.path.normpath(
                    os.path.join(app.confdir, index_template_path)
                )

            template_paths.insert(0, index_template_path)

        # Create the jinja environment to do the work
        jinja_env = Environment(loader=FileSystemLoader(template_paths),)

        output_path = app.config.autosaltsls_build_root
        if not os.path.abspath(output_path):
            output_path = os.path.join(app.confdir, output_path,)

        output_file = os.path.join(output_path, "index.rst")

        template_obj = jinja_env.get_template("master.rst_t")

        logger.debug(
            "[AutoSaltSLS] Rendering master index '{0}' using '{1}'".format(
                output_file, template_obj.filename,
            )
        )

        # Render the template using Jinja
        with open(output_file, "w") as outfile:
            outfile.write(
                template_obj.render(
                    project=app.config.project,
                    display_master_indices=app.config.autosaltsls_display_master_indices,
                )
            )


def config_autosaltsls(app, config):
    """
    Create custom source-specific Sphinx role/object types
    """
    logger.debug("JPH - {0}".format(config.autosaltsls_sources))
    if isinstance(config.autosaltsls_sources, dict):
        logger.debug("JPH - getting sources")
        for source, settings in config.autosaltsls_sources.items():
            logger.debug("JPH - {0}:{1}".format(source, settings))
            try:
                role = settings["cross_ref_role"]

                # Create sphinx objects for the source role
                app.add_object_type(
                    role,
                    role,
                    objname="{0} file".format(role),
                    indextemplate="pair: %s; {0} file".format(role),
                )

                logger.info(
                    bold("[AutoSaltSLS] ")
                    + "Adding custom Sphinx role/object type "
                    + darkgreen("{0}".format(role))
                )
            except KeyError:
                pass


def setup(app):
    """
    Setup the Sphinx app with the default config values and add the ``sls`` object type.
    """
    app.connect("builder-inited", run_autosaltsls)
    app.connect("config-inited", config_autosaltsls)

    app.add_config_value("autosaltsls_sources_root", "..", "env")
    app.add_config_value("autosaltsls_sources", None, "env")
    app.add_config_value("autosaltsls_doc_prefix", "###", "html")
    app.add_config_value("autosaltsls_comment_prefix", "#", "html")
    app.add_config_value("autosaltsls_comment_ignore_prefix", "#!", "html")
    app.add_config_value("autosaltsls_remove_first_space", True, "html")
    app.add_config_value("autosaltsls_source_url_root", None, "html")
    app.add_config_value("autosaltsls_build_root", ".", "env")
    app.add_config_value("autosaltsls_write_index_page", False, "env")
    app.add_config_value("autosaltsls_index_template_path", "", "env")
    app.add_config_value("autosaltsls_display_master_indices", True, "html")

    # Add an object type for the sls files
    app.add_object_type(
        "sls", "sls", objname="sls file", indextemplate="pair: %s; sls file"
    )
