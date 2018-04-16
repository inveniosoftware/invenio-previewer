# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Render a CSV file using d3.js."""

from __future__ import absolute_import, print_function

import csv

from flask import current_app, render_template

from ..proxies import current_previewer
from ..utils import detect_encoding

previewable_extensions = ['csv', 'dsv']


def validate_csv(file):
    """Return dialect information about given csv file."""
    try:
        # Detect encoding and dialect
        with file.open() as fp:
            encoding = detect_encoding(fp, default='utf-8')
            sample = fp.read(
                current_app.config.get('PREVIEWER_CSV_VALIDATION_BYTES', 1024))
            allowed_delimiters = current_app.config.get(
                'PREVIEWER_CSV_SNIFFER_ALLOWED_DELIMITERS', None)
            delimiter = csv.Sniffer().sniff(
                sample=sample.decode(encoding),
                delimiters=allowed_delimiters).delimiter
            is_valid = True
    except Exception as e:
        current_app.logger.debug(
            'File {0} is not valid CSV: {1}'.format(file.uri, e))
        encoding = ''
        delimiter = ''
        is_valid = False

    return {
        'delimiter': delimiter,
        'encoding': encoding,
        'is_valid': is_valid
    }


def can_preview(file):
    """Determine if the given file can be previewed."""
    if file.is_local() and file.has_extensions('.csv', '.dsv'):
        return validate_csv(file)['is_valid']
    return False


def preview(file):
    """Render the appropriate template with embed flag."""
    file_info = validate_csv(file)
    return render_template(
        'invenio_previewer/csv_bar.html',
        file=file,
        delimiter=file_info['delimiter'],
        encoding=file_info['encoding'],
        js_bundles=current_previewer.js_bundles + ['d3_csv.js'],
        css_bundles=current_previewer.css_bundles,
    )
