import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sphinxcontrib-autosaltsls',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='Apache 2',
    description='Sphinx auto-document generator for SaltStack sls files',
    long_description=README,
    url='https://bitbucket.tools.ficoccs-dev.net/projects/DEVOPS/repos/ccs-standard-templates/browse',
    author='John Hicks',
    author_email='johnhicks@fico.com',
    install_requires=[
        'Jinja2',
        'sphinx>=2.0.0'
    ],
)