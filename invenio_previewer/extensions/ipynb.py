# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Jupyter Notebook previewer."""

from __future__ import absolute_import, unicode_literals

import nbformat
from flask import render_template
from nbconvert import HTMLExporter

from ..proxies import current_previewer

previewable_extensions = ['ipynb']


def render(file):
    """Generate the result HTML."""
    with file.open() as fp:
        content = fp.read()

    notebook = nbformat.reads(content.decode("utf-8"), as_version=4)

    html_exporter = HTMLExporter()
    html_exporter.template_file = "base"
    (body, resources) = html_exporter.from_notebook_node(notebook)
    return body, resources


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions(".ipynb")


def preview(file):
    """Render the IPython Notebook."""
    body, resources = render(file)
    default_jupyter_nb_style = resources["inlining"]["css"][0]
    return render_template(
        "invenio_previewer/ipynb.html",
        file=file,
        content=body,
        inline_style=default_jupyter_nb_style,
        js_bundles=current_previewer.js_bundles,
        css_bundles=current_previewer.css_bundles,
    )
