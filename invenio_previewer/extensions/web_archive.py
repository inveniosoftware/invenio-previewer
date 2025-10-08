# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 New York University.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Web Archive rendering."""

from flask import current_app, render_template

from invenio_previewer.proxies import current_previewer

previewable_extensions = ["wacz", "warc", "har", "cdx", "cdxj"]


def can_preview(file):
    """Check if file can be previewed."""
    return file.is_local() and file.has_extensions(
        ".wacz", ".warc", ".warc.gz", ".har", ".cdx", ".cdxj"
    )


def preview(file):
    """Render Web Archive files."""
    return render_template(
        "invenio_previewer/web_archive.html",
        file=file,
        css_bundles=current_previewer.css_bundles + ["web_archive_css.css"],
        range_requests=current_app.config.get(
            "PREVIEWER_WEB_ARCHIVE_RANGE_REQUESTS", False
        ),
    )
