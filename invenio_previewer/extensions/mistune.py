# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Markdown rendering using mistune library."""

import bleach
import mistune
from flask import current_app, render_template

from ..proxies import current_previewer
from ..utils import detect_encoding

previewable_extensions = ["md"]


def render(file):
    """Render HTML from Markdown file content."""
    with file.open() as fp:
        encoding = detect_encoding(fp, default="utf-8")
        try:
            result = mistune.markdown(fp.read().decode(encoding))
            return result
        except Exception as e:
            current_app.logger.exception(str(e))
            return None


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions(".md")


def preview(file):
    """Render Markdown."""
    content = render(file)
    if content is not None:
        return render_template(
            "invenio_previewer/mistune.html",
            file=file,
            content=content,
            js_bundles=current_previewer.js_bundles,
            css_bundles=current_previewer.css_bundles,
        )
    else:
        return render_template("invenio_previewer/default.html")
