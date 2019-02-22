# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""IPython notebooks previewer."""

from __future__ import absolute_import, unicode_literals

import nbformat
from flask import render_template
from nbconvert import HTMLExporter


def render(file):
    """Generate the result HTML."""
    fp = file.open()
    content = fp.read()
    fp.close()

    notebook = nbformat.reads(content.decode('utf-8'), as_version=4)

    html_exporter = HTMLExporter()
    html_exporter.template_file = 'basic'
    (body, resources) = html_exporter.from_notebook_node(notebook)
    return body, resources


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions('.ipynb')


def preview(file):
    """Render the IPython Notebook."""
    body, resources = render(file)
    default_ipython_style = resources['inlining']['css'][1]
    return render_template(
        'invenio_previewer/ipynb.html',
        file=file,
        content=body,
        style=default_ipython_style
    )
