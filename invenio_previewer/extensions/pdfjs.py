# SPDX-FileCopyrightText: 2015-2019 CERN.
# SPDX-License-Identifier: MIT

"""PDF previewer based on pdf.js."""

from flask import render_template

from ..proxies import current_previewer

previewable_extensions = ["pdf", "pdfa"]


def can_preview(file):
    """Check if file can be previewed."""
    return file.has_extensions(".pdf", ".pdfa")


def preview(file):
    """Preview file."""
    return render_template(
        "invenio_previewer/pdfjs.html",
        file=file,
        html_tags='dir="ltr" mozdisallowselectionprint moznomarginboxes',
        css_bundles=[],
        js_bundles=current_previewer.js_bundles,
    )
