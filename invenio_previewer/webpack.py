# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""JS/CSS bundles for Previewer."""

from __future__ import absolute_import, print_function

from invenio_assets.webpack import WebpackThemeBundle

previewer = WebpackThemeBundle(
    __name__,
    'assets',
    default='semantic-ui',
    themes={
        'bootstrap3': dict(
            entry={
                'd3_csv': './js/csv_previewer/init.js',
                'previewer_theme': './js/previewer_theme.js',
                'fullscreen_js': './js/fullscreen.js',
                'prism_js': './js/prismjs.js',
                'prism_css': './scss/prismjs.scss',
                'pdfjs_js': './js/pdfjs.js',
                'pdfjs_css': './scss/pdfjs.scss',
                'simple_image_css': './scss/simple_image.scss'
            },
            dependencies={
                'bootstrap-sass': '~3.4.0',
                'd3': '^3.5.17',
                'flightjs': '~1.5.1',
                'font-awesome': '~4.5.0',
                'jquery': '^3.3.1',
                'pdfjs-dist': '^1.4.192',
                'prismjs': '^1.15.0',
            }
        ),
        'semantic-ui': dict(
            entry={
                'd3_csv': './js/invenio_previewer/csv_previewer/init.js',
                'previewer_theme': './js/invenio_previewer/previewer_theme.js',
                'fullscreen_js': './js/invenio_previewer/fullscreen.js',
                'prism_js': './js/invenio_previewer/prismjs.js',
                'prism_css': './scss/invenio_previewer/prismjs.scss',
                'pdfjs_js': './js/invenio_previewer/pdfjs.js',
                'pdfjs_css': './scss/invenio_previewer/pdfjs.scss',
                'simple_image_css':
                    './scss/invenio_previewer/simple_image.scss'
            },
            dependencies={
                'd3': '^3.5.17',
                'flightjs': '~1.5.1',
                'font-awesome': '~4.5.0',
                'jquery': '^3.3.1',
                'pdfjs-dist': '^1.4.192',
                'prismjs': '^1.15.0',
            }
        ),
    }
)
"""Bundle of webpack assets."""
