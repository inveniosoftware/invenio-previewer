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
"""Maximum file size in bytes for previewers that load entire files into memory."""

PREVIEWER_MAX_IMAGE_SIZE_BYTES = 0.5 * 1024 * 1024
"""Maximum file size in bytes for image files."""

PREVIEWER_TXT_MAX_BYTES = 1 * 1024 * 1024
"""Maximum number of .txt file bytes to preview before truncated."""

PREVIEWER_CSV_MAX_BYTES = 100 * 1024 * 1024
"""Maximum file size in bytes for CSV files."""

PREVIEWER_ZIP_MAX_FILES = 1000
"""Max number of files showed in the ZIP previewer."""

PREVIEWER_ZIP_MAX_BYTES = 100 * 1024 * 1024
"""Max size of ZIP file showed in the ZIP previewer."""

PREVIEWER_CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    # Allow images from any site. Notebooks, Markdown files and GeoJSON map
    # tiles show images from other sites, and an image can't run code.
    "img-src": ["*", "data:", "blob:"],
    "font-src": ["'self'", "data:"],
    "connect-src": ["'self'"],
    "media-src": ["'self'", "blob:"],
    "worker-src": ["'self'", "blob:"],
    "object-src": ["'none'"],
    "base-uri": ["'none'"],
    "form-action": ["'self'"],
}
"""Content-Security-Policy applied to file previews.

This policy goes in a ``<meta http-equiv="Content-Security-Policy">`` tag in
the preview page. It is not sent as an HTTP header. Browsers ignore some rules
in a meta tag, like ``frame-ancestors``, ``report-uri`` and ``sandbox``. Those
have to be set in the HTTP header instead.
:func:`invenio_previewer.response.preview_response` does this for ``sandbox``.

``script-src`` has neither ``'unsafe-inline'`` nor ``'unsafe-eval'``, so
scripts written inside the page and ``eval()`` are blocked. Only script files
from our own site run.

Set it to ``None`` to turn the policy off.
"""

PREVIEWER_EXTERNAL_DOMAINS = []
"""Set the external domains that previews may load files from.

You need this when file downloads redirect to another domain, for example to
the links of an S3 storage. Use the scheme, host and port of the redirect,
without the path. For example
``["https://my-bucket.s3.eu-west-1.amazonaws.com"]``.

If ``S3_ENDPOINT_URL`` of Invenio-S3 is set, its domain is added for you. So
you only need this for AWS S3, where ``S3_ENDPOINT_URL`` is not set, or when
the browser reaches the storage on a different domain than
``S3_ENDPOINT_URL``.

The domains are only added to ``connect-src`` and ``media-src``. Files from
them can be downloaded and played, but never run as scripts. Use the exact
host of your bucket, not a wildcard like ``https://*.s3.amazonaws.com``, which
allows any bucket.
"""

PREVIEWER_SANDBOX = "allow-scripts allow-popups allow-popups-to-escape-sandbox"
"""Sandbox for previews whose previewer has ``sandbox = True``.

The browser isolates a sandboxed preview from the site: it has no access to
the user's cookies or session. So a malicious uploaded file can't act as the
logged-in user.

The value is a list of things the sandbox still allows:

- ``allow-scripts``: some previews need JavaScript, for example for code
  highlighting. This is safe, because the scripts run isolated from the site.
- ``allow-popups allow-popups-to-escape-sandbox``: links in a preview can
  open in a new tab, as a normal page.

Never add ``allow-same-origin``. Together with ``allow-scripts`` it lets the
preview's scripts remove the sandbox, so the preview is not isolated anymore.

This value is used in two places:

- the ``sandbox`` rule of the preview's Content-Security-Policy HTTP header,
  set by :func:`invenio_previewer.response.preview_response`.
- the ``sandbox`` attribute of the preview ``<iframe>``.

Set it to ``None`` to turn sandboxing off.
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
