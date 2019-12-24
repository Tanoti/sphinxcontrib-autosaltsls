import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='sphinxcontrib-autosaltsls',
    version='0.4.0',
    packages=['sphinxcontrib.autosaltsls'],
    include_package_data=True,
    license='Apache 2',
    description='Sphinx auto-document generator for SaltStack sls files',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/Tanoti/sphinxcontrib-autosaltsls',
    author='John Hicks',
    author_email='john.p.hicks@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Documentation',
    ],
    install_requires=[
        'Jinja2',
        'sphinx>=2.0.0'
    ],
)
