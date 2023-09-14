# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Render a CSV file using Papaparse."""

from flask import current_app, render_template

from ..proxies import current_previewer

previewable_extensions = ["csv", "dsv"]


def validate_csv(file):
    """Return dialect information about given csv file."""
    max_file_size = current_app.config.get(
        "PREVIEWER_MAX_FILE_SIZE_BYTES", 10 * 1024 * 1024
    )
    is_size_valid = file.size <= max_file_size
    return is_size_valid


def can_preview(file):
    """Determine if the given file can be previewed."""
    return (
        file.is_local() and file.has_extensions(".csv", ".dsv") and validate_csv(file)
    )


def preview(file):
    """Render the appropriate template with embed flag."""
    return render_template(
        "invenio_previewer/csv_bar.html",
        file=file,
        js_bundles=current_previewer.js_bundles + ["papaparse_csv.js"],
        css_bundles=current_previewer.css_bundles,
    )
