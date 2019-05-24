# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Previewer bundles.

.. deprecated:: 1.0.0
    AMD/RequireJS based bundles have been deprecated in Invenio v3.0 and will
    be removed.
"""

from __future__ import unicode_literals

from flask_assets import Bundle
from invenio_assets import NpmBundle, RequireJSFilter

previewer_base_css = Bundle(
    "node_modules/bootstrap/dist/css/bootstrap.css",
    NpmBundle(
        npm={
            "bootstrap-sass": "~3.4.0",
            "font-awesome": "~4.5.0",
        }
    ),
    output='gen/previewer-base.%(version)s.css'
)
"""CSS bundle for ZIP file previewer."""


previewer_base_js = Bundle(
    NpmBundle(
        npm={
            "jquery": "~3.3.0",
            "bootstrap": "~3.4.0",
        }
    ),
    "node_modules/jquery/dist/jquery.js",
    "node_modules/bootstrap/dist/js/bootstrap.js",
    output='gen/previewer-base.%(version)s.js',
)
"""JavaScript bundle for basic tools."""

csv_previewer_js = Bundle(
    "node_modules/requirejs/require.js",
    NpmBundle(
        npm={
            "requirejs": "~2.3.6",
            "flightjs": "~1.5.1",
            "d3": "~3.5.17",
            "jquery": "~3.3.0"
        }
    ),
    Bundle(
        "js/csv_previewer/init.js",
        filters=RequireJSFilter(optimize='none'),
    ),
    output="gen/csv_previewer.%(version)s.js",
)
"""JavaScript bundle for D3.js CSV previewer."""

pdfjs_css = Bundle(
    "css/pdfjs/viewer.css",
    output='gen/pdfjs.%(version)s.css',
)
"""CSS bundle for PDFjs previewer."""

pdfjs_js = Bundle(
    NpmBundle(
        npm={
            "pdfjs-dist": "^1.4.192",
        }
    ),
    "node_modules/pdfjs-dist/web/compatibility.js",
    "node_modules/pdfjs-dist/build/pdf.js",
    "js/pdfjs/l10n.js",
    "js/pdfjs/viewer.js",
    output='gen/pdfjs.%(version)s.js',
)
"""JavaScript bundle for PDFjs previewer."""

fullscreen_js = Bundle(
    "js/zip/fullscreen.js",
    filters='uglifyjs',
    output='gen/fullscreen.%(version)s.js',
)
"""JavaScript bundle for ZIP file previewer."""

prism_js = Bundle(
    NpmBundle(
        npm={
            "prismjs": "^1.15.0",
        },
    ),
    "node_modules/prismjs/prism.js",
    "node_modules/prismjs/components/prism-json.js",
    filters="uglifyjs",
    output='gen/prism.%(version)s.js',
)
"""JavaScript bundle for prism.js syntax highlighter."""

prism_css = Bundle(
    NpmBundle(
        npm={
            "prismjs": "^1.15.0",
        },
    ),
    "node_modules/prismjs/themes/prism.css",
    "css/prismjs/simple.css",
    output='gen/prism.%(version)s.css'
)
"""CSS bundle for prism.js syntax highlighter."""
