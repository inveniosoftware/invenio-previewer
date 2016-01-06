# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
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

"""Previewer bundles."""

from __future__ import unicode_literals

from flask_assets import Bundle
from invenio_assets import NpmBundle, RequireJSFilter

csv_previewer_js = Bundle(
    NpmBundle(
        'node_modules/almond/almond.js',
        npm={
            "almond": "~0.3.1",
            "jquery": "~1.9.1",
            "flightjs": "~1.5.1",
            "d3": "~3.5.12",
        }
    ),
    Bundle(
        "js/csv_previewer/init.js",
        filters=RequireJSFilter(optimize='none'),
    ),
    output="gen/csv_previewer.%(version)s.js",
)

pdfjs_css = Bundle(
    "css/pdfjs/viewer.css",
    output='gen/pdfjs.%(version)s.css',
)

pdfjs_worker_js = Bundle(
    NpmBundle(
        npm={
            "pdf-viewer": "0.8.1",  # PDFJS. It doesn't have an official repo.
        }
    ),
    "node_modules/pdf-viewer/ready/generic/build/pdf.worker.js",
    output='gen/pdfjs.worker.js',
)

pdfjs_js = Bundle(
    NpmBundle(
        npm={
            "jquery": "~1.9.1",
            "pdf-viewer": "0.8.1",  # PDFJS. It doesn't have an official repo.
        }
    ),
    "node_modules/jquery/jquery.js",
    "node_modules/pdf-viewer/ready/generic/web/compatibility.js",
    "node_modules/pdf-viewer/ready/generic/web/l10n.js",
    "node_modules/pdf-viewer/ready/generic/web/viewer.js",
    "node_modules/pdf-viewer/ready/generic/build/pdf.js",
    "node_modules/pdf-viewer/ready/generic/build/pdf.worker.js",
    "js/pdfjs/pdf_viewer.js",
    output='gen/pdfjs.%(version)s.js',
)

zip_css = Bundle(
    "node_modules/bootstrap/dist/css/bootstrap.css",
    NpmBundle(
        npm={
            "bootstrap": "~3.3.6",
            "font-awesome": "~4.5.0",
        }
    ),
    output='gen/zip.%(version)s.css'
)

zip_js = Bundle(
    NpmBundle(
        npm={
             "jquery": "~1.9.1",
        }
    ),
    "node_modules/jquery/jquery.js",
    "js/zip/fullscreen.js",
    output='gen/zip.%(version)s.js',
)
