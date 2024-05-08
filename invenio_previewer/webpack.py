# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
# Copyright (C)      2022 TU Wien.
# Copyright (C)      2023 Northwestern University.
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

from invenio_assets.webpack import WebpackThemeBundle

previewer = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "bootstrap3": dict(
            entry={
                "papaparse_csv": "./js/invenio_previewer/csv_previewer/init.js",
                "previewer_theme": "./js/invenio_previewer/previewer_theme.js",
                "prism_js": "./js/invenio_previewer/prismjs.js",
                "prism_css": "./scss/invenio_previewer/prismjs.scss",
                "simple_image_css": "./scss/invenio_previewer/simple_image.scss",
            },
            dependencies={
                "bootstrap-sass": "~3.3.5",
                "papaparse": "^5.4.1",
                "flightjs": "~1.5.1",
                "font-awesome": "~4.5.0",
                "jquery": "^3.3.1",
                "pdfjs-dist": "^4.0",
                "prismjs": "^1.15.0",
            },
            aliases={
                "@scss/invenio_previewer": "scss/invenio_previewer",
            },
            copy=[
                # Copy the pdfjs-dist artifacts from `node_modules` into `static`
                {
                    "from": "../node_modules/pdfjs-dist/build",
                    "to": "../../static/js/pdfjs/build",
                },
                {
                    "from": "../node_modules/pdfjs-dist/cmaps",
                    "to": "../../static/js/pdfjs/cmaps",
                },
                {
                    "from": "../node_modules/pdfjs-dist/web",
                    "to": "../../static/js/pdfjs/web",
                },
            ],
        ),
        "semantic-ui": dict(
            entry={
                "papaparse_csv": "./js/invenio_previewer/csv_previewer/init.js",
                "previewer_theme": "./js/invenio_previewer/previewer_theme.js",
                "prism_js": "./js/invenio_previewer/prismjs.js",
                "prism_css": "./scss/invenio_previewer/prismjs.scss",
                "bottom_js": "./js/invenio_previewer/bottom.js",
                "zip_css": "./scss/invenio_previewer/zip.scss",
                "bottom_css": "./scss/invenio_previewer/bottom.scss",
                "simple_image_css": "./scss/invenio_previewer/simple_image.scss",
                "txt_css": "./scss/invenio_previewer/txt.scss",
                "videojs_js": "./node_modules/video.js/dist/video.min.js",
                "audio_videojs_css": "./scss/invenio_previewer/audio_videojs.scss",
                "video_videojs_css": "./scss/invenio_previewer/video_videojs.scss",
            },
            dependencies={
                "flightjs": "~1.5.1",
                "font-awesome": "~4.5.0",
                "jquery": "^3.3.1",
                "papaparse": "^5.4.1",
                "prismjs": "^1.15.0",
                "video.js": "^8.6.1",
                "pdfjs-dist": "^4.0",
            },
            copy=[
                # Copy the pdfjs-dist artifacts from `node_modules` into `static`
                {
                    "from": "../node_modules/pdfjs-dist/build",
                    "to": "../../static/js/pdfjs/build",
                },
                {
                    "from": "../node_modules/pdfjs-dist/cmaps",
                    "to": "../../static/js/pdfjs/cmaps",
                },
                {
                    "from": "../node_modules/pdfjs-dist/web",
                    "to": "../../static/js/pdfjs/web",
                },
            ],
        ),
    },
)
"""Bundle of webpack assets."""
