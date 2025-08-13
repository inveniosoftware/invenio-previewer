# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Package configuration."""

PREVIEWER_CSV_VALIDATION_BYTES = 1024
"""Number of bytes read by CSV previewer to validate the file."""

PREVIEWER_CSV_SNIFFER_ALLOWED_DELIMITERS = None
"""Allowed delimiter characters passed to the ``csv.Sniffer.sniff`` method."""

PREVIEWER_CHARDET_BYTES = 1024
"""Number of bytes to read for character encoding detection by `cchardet`."""

PREVIEWER_CHARDET_CONFIDENCE = 0.9
"""Confidence threshold for character encoding detection by `cchardet`."""

PREVIEWER_MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024
"""Maximum file size in bytes for JSON/XML files."""

PREVIEWER_MAX_IMAGE_SIZE_BYTES = 0.5 * 1024 * 1024
"""Maximum file size in bytes for image files."""

PREVIEWER_TXT_MAX_BYTES = 1 * 1024 * 1024
"""Maximum number of .txt file bytes to preview before truncated."""

PREVIEWER_CSV_MAX_BYTES = 100 * 1024 * 1024
"""Maximum file size in bytes for CSV files."""

PREVIEWER_ZIP_MAX_FILES = 1000
"""Max number of files showed in the ZIP previewer."""

PREVIEWER_PDF_JS_ENABLE_SCRIPTING = False
"""Enable JavaScript execution in PDF files (disabled by default for security)."""

PREVIEWER_IFRAME_SANDBOX_ATTRIBUTES = [
    # Required for previewers to access their own content and make same-origin requests
    "allow-same-origin",
    # Allows form submission within previewers (e.g., search functionality in PDF viewer)
    "allow-forms",
    # Enables opening links in new windows/tabs from preview content
    "allow-popups",
    # Allows popups to escape sandbox restrictions (so external links open normally)
    "allow-popups-to-escape-sandbox",
    # Permits download functionality from within the previewer
    "allow-downloads",
    # NOTE: "allow-scripts" is intentionally omitted by default to prevent JavaScript
    # execution as a security measure. Add it to this list if you need to enable
    # JavaScript in preview iframes (not recommended for security reasons).
]
"""Sandbox attributes for preview iframes (secure by default configuration)."""

PREVIEWER_PREFERENCE = [
    "csv_papaparsejs",
    "simple_image",
    "json_prismjs",
    "xml_prismjs",
    "mistune",
    "pdfjs",
    "video_videojs",
    "audio_videojs",
    "ipynb",
    "zip",
    "txt",
]
"""Decides which previewers are available and their priority."""

PREVIEWER_ABSTRACT_TEMPLATE = "invenio_previewer/abstract_previewer.html"
"""Parent template used by the available previewers."""

PREVIEWER_BASE_CSS_BUNDLES = ["previewer_theme.css"]
"""Basic bundle which includes Font-Awesome/Bootstrap."""

PREVIEWER_BASE_JS_BUNDLES = ["previewer_theme.js"]
"""Basic bundle which includes Bootstrap/jQuery."""

PREVIEWER_RECORD_FILE_FACOTRY = None
"""Factory for extracting files from records."""
