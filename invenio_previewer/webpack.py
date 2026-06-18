# SPDX-FileCopyrightText: 2016-2022 CERN.
# SPDX-FileCopyrightText: 2022 TU Wien.
# SPDX-FileCopyrightText: 2023 Northwestern University.
# SPDX-FileCopyrightText: 2025 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""JS/CSS bundles for Previewer."""

from invenio_assets.webpack import WebpackThemeBundle

previewer = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "bootstrap3": dict(
            entry={
                "geojson_js": "./js/invenio_previewer/geojson.js",
                "geojson_css": "./scss/invenio_previewer/geojson.scss",
                "papaparse_csv": "./js/invenio_previewer/csv_previewer/init.js",
                "previewer_theme": "./js/invenio_previewer/previewer_theme.js",
                "prism_js": "./js/invenio_previewer/prismjs.js",
                "prism_css": "./scss/invenio_previewer/prismjs.scss",
                "simple_image_css": "./scss/invenio_previewer/simple_image.scss",
                "web_archive_css": "./scss/invenio_previewer/web_archive.scss",
            },
            dependencies={
                "@mikespub/epubjs-reader": "^2026.1.24",
                "bootstrap-sass": "~3.3.5",
                "leaflet": "^1.9.4",
                "papaparse": "^5.4.1",
                "flightjs": "~1.5.1",
                "font-awesome": "~4.5.0",
                "jquery": "^3.3.1",
                "pdfjs-dist": "^5.0",
                "prismjs": "^1.15.0",
                "replaywebpage": "^2.3.16",
            },
            aliases={
                "@scss/invenio_previewer": "scss/invenio_previewer",
            },
            copy=[
                # Copy the pdfjs-dist artifacts from `node_modules` into `static`
                {
                    "from": "../node_modules/pdfjs-dist/legacy/build",
                    "to": "../../static/js/pdfjs/build",
                },
                {
                    "from": "../node_modules/pdfjs-dist/cmaps",
                    "to": "../../static/js/pdfjs/cmaps",
                },
                {
                    "from": "../node_modules/pdfjs-dist/wasm",
                    "to": "../../static/js/pdfjs/wasm",
                },
                {
                    "from": "../node_modules/pdfjs-dist/legacy/web",
                    "to": "../../static/js/pdfjs/web",
                },
                {
                    "from": "../node_modules/replaywebpage",
                    "to": "../../static/js/replaywebpage",
                },
                {
                    "from": "../node_modules/@mikespub/epubjs-reader/dist/assets",
                    "to": "../../static/epubreader/assets",
                },
                {
                    "from": "../node_modules/@mikespub/epubjs-reader/dist/js",
                    "to": "../../static/epubreader/js",
                },
            ],
        ),
        "semantic-ui": dict(
            entry={
                "geojson_js": "./js/invenio_previewer/geojson.js",
                "geojson_css": "./scss/invenio_previewer/geojson.scss",
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
                "web_archive_css": "./scss/invenio_previewer/web_archive.scss",
            },
            dependencies={
                "@mikespub/epubjs-reader": "^2026.1.24",
                "ajv": "^8.0.0",
                "flightjs": "~1.5.1",
                "font-awesome": "~4.5.0",
                "jquery": "^3.3.1",
                "leaflet": "^1.9.4",
                "papaparse": "^5.4.1",
                "prismjs": "^1.15.0",
                "video.js": "^8.6.1",
                "pdfjs-dist": "^5.0",
                "replaywebpage": "^2.3.16",
            },
            copy=[
                # Copy the pdfjs-dist artifacts from `node_modules` into `static`
                {
                    "from": "../node_modules/pdfjs-dist/legacy/build",
                    "to": "../../static/js/pdfjs/build",
                },
                {
                    "from": "../node_modules/pdfjs-dist/cmaps",
                    "to": "../../static/js/pdfjs/cmaps",
                },
                {
                    "from": "../node_modules/pdfjs-dist/wasm",
                    "to": "../../static/js/pdfjs/wasm",
                },
                {
                    "from": "../node_modules/pdfjs-dist/legacy/web",
                    "to": "../../static/js/pdfjs/web",
                },
                {
                    "from": "../node_modules/replaywebpage",
                    "to": "../../static/js/replaywebpage",
                },
                {
                    "from": "../node_modules/@mikespub/epubjs-reader/dist/assets",
                    "to": "../../static/epubreader/assets",
                },
                {
                    "from": "../node_modules/@mikespub/epubjs-reader/dist/js",
                    "to": "../../static/epubreader/js",
                },
            ],
        ),
    },
)
"""Bundle of webpack assets."""
