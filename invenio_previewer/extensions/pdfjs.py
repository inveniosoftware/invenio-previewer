# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""PDF previewer based on pdf.js."""

from __future__ import absolute_import, print_function

from flask import render_template

from ..proxies import current_previewer

previewable_extensions = ['pdf', 'pdfa']


def can_preview(file):
    """Check if file can be previewed."""
    return file.has_extensions('.pdf', '.pdfa')


def preview(file):
    """Preview file."""
    return render_template(
        'invenio_previewer/pdfjs.html',
        file=file,
        css_bundles=['previewer_pdfjs_css'],
        js_bundles=[
            'previewer_pdfjs_js',
            'previewer_fullscreen_js'
        ] + current_previewer.js_bundles,
    )
