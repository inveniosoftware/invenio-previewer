# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
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
    'check-manifest>=0.25',
    'coverage>=4.5.3',
    'invenio-config>=1.0.2',
    'invenio-db[versioning]>=1.0.2',
    'isort>=4.3.4',
    'mock>=1.3.0',
    'pydocstyle>=1.0.0',
    'pytest-cov>=2.7.1',
    'pytest-pep8>=1.0.6',
    'pytest>=4.6.4,<5.0.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'files': [
        'invenio-files-rest>=1.0.0',
        'invenio-records-files>=1.0.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'cchardet>=1.0.0',
    'Flask-BabelEx>=0.9.3',
    'Flask>=0.11.1',
    'invenio-assets>=1.1.2',
    'invenio-formatter>=1.0.2',
    'invenio-pidstore>=1.0.0',
    'invenio-records-ui>=1.0.1',
    'ipython>=4.1.0',
    'mistune>=0.7.2',
    'nbconvert[execute]>=4.1.0',
    'nbformat>=4.0.1',
    'tornado>=4.1,<=5.1.1',  # required by nbconvert -> jupyter-client
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
        'invenio_assets.bundles': [
            'previewer_theme.css = '
            'invenio_previewer.bundles:previewer_base_css',
            'previewer_theme.js = invenio_previewer.bundles:previewer_base_js',
            'd3_csv.js = invenio_previewer.bundles:csv_previewer_js',
            'pdfjs_css.css = invenio_previewer.bundles:pdfjs_css',
            'pdfjs_js.js = invenio_previewer.bundles:pdfjs_js',
            'fullscreen_js.js = invenio_previewer.bundles:fullscreen_js',
            'prism_js.js = invenio_previewer.bundles:prism_js',
            'prism_css.css = invenio_previewer.bundles:prism_css',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
