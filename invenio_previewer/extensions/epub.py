# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2026 CERN.
# Copyright (C) 2026 Front Matter.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""EPUB previewer based on epubjs-reader."""

from flask import render_template

from ..proxies import current_previewer

previewable_extensions = ["epub"]


def can_preview(file):
    """Check if file can be previewed."""
    return file.is_local() and file.has_extensions(".epub")


def preview(file):
    """Preview EPUB file."""
    return render_template(
        "invenio_previewer/epub.html",
        book_path=file.uri,
        file=file,
        css_bundles=current_previewer.css_bundles,
        js_bundles=current_previewer.js_bundles,
    )
