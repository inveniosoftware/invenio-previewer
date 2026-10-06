# SPDX-FileCopyrightText: 2015-2026 CERN.
# SPDX-License-Identifier: MIT

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

PREVIEWER_CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    # images cannot run scirpts, and notebooks, markdown files and the GeoJSON
    # map tiles load them from other hosts
    "img-src": ["*", "data:", "blob:"],
    "font-src": ["'self'", "data:"],
    "media-src": ["'self'", "blob:"],
    "worker-src": ["'self'", "blob:"],
    "object-src": ["'none'"],
    "base-uri": ["'none'"],
    "form-action": ["'self'"],
}
"""Content-Security-Policy applied to file previws.

`script-src` does not allow `unsafie-inline` nor `unsafe-eval`.
"""

PREVIEWER_PDF_JS_ENABLE_SCRIPTING = False
"""Enable JavaScript execution in PDF files (disabled by default for security)."""

PREVIEWER_PDF_JS_DOCUMENT_INIT_PARAMS = None
"""Additional DocumentInitParameters passed to pdfjsLib.getDocument().

See https://mozilla.github.io/pdf.js/api/draft/module-pdfjsLib.html for the full
list of available options.

Example (disable range requests, streaming, and auto-fetching)::

    PREVIEWER_PDF_JS_DOCUMENT_INIT_PARAMS = {
        "disableStream": True,
        "disableRange": True,
        "disableAutoFetch": True,
    }
"""

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
    # "web_archive",
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

PREVIEWER_WEB_ARCHIVE_RANGE_REQUESTS = False
"""Whether the file server supports range requests or not."""
