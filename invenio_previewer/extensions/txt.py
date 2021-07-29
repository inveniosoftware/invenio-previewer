# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2021 Northwestern University.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Text rendering."""

from flask import render_template

from ..proxies import current_previewer
from ..utils import detect_encoding

previewable_extensions = ["txt"]


def render(file):
    """Render HTML from txt file content."""
    with file.open() as fp:
        encoding = detect_encoding(fp, default="utf-8")
        return fp.read().decode(encoding)


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions(
        *[f".{ext}" for ext in previewable_extensions]
    )


def preview(file):
    """Render Markdown."""
    return render_template(
        "invenio_previewer/txt.html",
        file=file,
        content=render(file),
        js_bundles=current_previewer.js_bundles,
        css_bundles=current_previewer.css_bundles,
    )
