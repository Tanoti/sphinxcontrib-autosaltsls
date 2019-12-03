"""
Sphinx Auto-SaltSLS top-level extension
"""
from sphinx.errors import ExtensionError
from sphinx.util import logging

from .mapper import AutoSaltSLSMapper

__author__ = """John Hicks"""
__email__ = 'johnhicks@fico.com'
__version__ = '0.1.0'

SETTINGS_STRING = [
    'title',
    'template_path',
    'build_dir',
    'url_root',
    'prefix',
]

logger = logging.getLogger(__name__)


def run_autosaltsls(app):
    """
    Load AutoSaltSLS data from the filesystem
    """
    logger.debug('[AutoSaltSLS] Starting')

    if not app.config.autosaltsls_sources:
        raise ExtensionError('No autosaltsls_sources setting found in config')

    sources = {}

    # Convert str or list into dict
    if isinstance(app.config.autosaltsls_sources, dict):
        sources = app.config.autosaltsls_sources
    elif isinstance(app.config.autosaltsls_sources, str):
        sources[app.config.autosaltsls_sources] = {}
    elif isinstance(app.config.autosaltsls_sources, list):
        for source in app.config.autosaltsls_sources:
            sources[source] = {}

    # Check the config options
    for source, settings in sources.items():
        if not isinstance(settings, dict):
            raise ExtensionError("Settings for '{0}' in autosaltsls_sources must be a dict".format(source))

        if 'exclude' in settings and not isinstance(settings['exclude'], list):
            raise ExtensionError(
                "Entry 'exclude' for '{0}' in autosaltsls_sources setting must be a list".format(
                    source
                )
            )

        # Check the str type settings
        for key in SETTINGS_STRING:
            if key in settings and not isinstance(settings[key], str):
                raise ExtensionError(
                    "Entry '{0}' for '{1}' in autosaltsls_sources setting must be a string".format(
                        key,
                        source,
                    )
                )

    # Loop over the sources and do the work
    for source, settings in sources.items():
        # Create a mapper for the source
        sphinx_mapper = AutoSaltSLSMapper(app, source, settings)

        # Scan the files in the source to build an object list
        sphinx_mapper.scan()

        # Load the sls file contents into their respective objects
        sphinx_mapper.load()

        # Write the rst files in the correct order
        sphinx_mapper.write()


def setup(app):
    app.connect("builder-inited", run_autosaltsls)

    app.add_config_value('autosaltsls_sources_root', '..', 'env')
    app.add_config_value('autosaltsls_sources', None, 'env')
    app.add_config_value('autosaltsls_doc_prefix', '###', 'html')
    app.add_config_value('autosaltsls_comment_prefix', '#', 'html')
    app.add_config_value('autosaltsls_comment_ignore_prefix', '#!', 'html')
    app.add_config_value('autosaltsls_remove_first_space', True, 'html')
    app.add_config_value('autosaltsls_source_url_root', None, 'html')
    app.add_config_value('autosaltsls_build_root', '.', 'env')

    app.add_object_type('sls', 'sls', objname='sls file', indextemplate='pair: %s; sls file')
