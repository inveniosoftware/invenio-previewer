# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for previewing files."""

import os

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand  # noqa

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'invenio-config>=1.0.3',
    'invenio-theme>=1.3.20',
    'invenio-db[versioning]>=1.0.14',
    'mock>=1.3.0',
    'pytest-invenio>=1.4.5',
]

extras_require = {
    'docs': [
        'Sphinx>=4.2.0,<5.0.0',
    ],
    'files': [
        'invenio-files-rest>=1.3.2',
        'invenio-records-files>=1.2.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'cchardet>=1.0.0',
    'invenio-assets>=1.2.7',
    'invenio-base>=1.2.11',
    'invenio-formatter>=1.1.3',
    'invenio-i18n>=2.0.0',
    'invenio-pidstore>=1.2.3',
    'invenio-records-ui>=1.2.0',
    'ipython>=4.1.0',
    'mistune>=0.8.1',
    # NOTE: nbclient package provides execute in nbconvert >= 6.X
    'nbconvert>=6.0,<7.0',
    'nbclient>=0.5,<1.0',
    'nbformat>=5.1,<6.0',
    'tornado>=6.1,<7.0',  # required by nbconvert -> jupyter-client
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_previewer', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-previewer',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio previewer',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-previewer',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_previewer = invenio_previewer:InvenioPreviewer',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_previewer',
        ],
        'invenio_assets.webpack': {
            'invenio_previewer_theme = invenio_previewer.webpack:previewer'
        },
        'invenio_previewer.previewers': [
            'csv_dthreejs = invenio_previewer.extensions.csv_dthreejs',
            'json_prismjs = invenio_previewer.extensions.json_prismjs',
            'simple_image = invenio_previewer.extensions.simple_image',
            'xml_prismjs = invenio_previewer.extensions.xml_prismjs',
            'mistune = invenio_previewer.extensions.mistune',
            'txt = invenio_previewer.extensions.txt',
            'pdfjs = invenio_previewer.extensions.pdfjs',
            'zip = invenio_previewer.extensions.zip',
            'ipynb = invenio_previewer.extensions.ipynb',
            'default = invenio_previewer.extensions.default',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
