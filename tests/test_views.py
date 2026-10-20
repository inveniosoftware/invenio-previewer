# SPDX-FileCopyrightText: 2016-2019 CERN.
# SPDX-License-Identifier: MIT

"""Views module tests."""

from io import BytesIO

import pytest
from flask import Flask, render_template_string

from invenio_previewer.api import PreviewFile
from invenio_previewer.extensions import ipynb, mistune


@pytest.mark.parametrize("previewer, extension", [(ipynb, "ipynb"), (mistune, "md")])
@pytest.mark.parametrize("limit", [None, 5])
@pytest.mark.parametrize("offset, expected", [(-1, True), (0, True), (1, False)])
def test_server_previewer_size_limit(
    record, previewer, extension, limit, offset, expected
):
    """Reject oversized notebooks and Markdown before rendering their content."""
    app = Flask(__name__)
    if limit is not None:
        app.config["PREVIEWER_MAX_FILE_SIZE_BYTES"] = limit
    size = (1024 * 1024 if limit is None else limit) + offset
    filename = f"test.{extension}"
    record.files[filename] = BytesIO(b" " * size)
    file = PreviewFile(None, record, record.files[filename])

    with app.app_context():
        assert previewer.can_preview(file) is expected


def test_view_macro_file_list(testapp):
    """Test file list macro."""
    with testapp.test_request_context():
        files = [
            {
                "key": "test1.txt",
                "size": 10,
                "date": "2016-07-12",
            },
            {
                "key": "test2.txt",
                "size": 12000000,
                "date": "2016-07-12",
            },
        ]

        pid = {"pid_value": 1}

        result = render_template_string(
            """
            {%- from "invenio_previewer/macros.html" import file_list %}
            {{ file_list(files, pid) }}
            """,
            files=files,
            pid=pid,
        )

        assert 'href="/record/1/files/test1.txt?download=1"' in result
        assert "<td>10 Bytes</td>" in result
        assert 'href="/record/1/files/test2.txt?download=1"' in result
        assert "<td>12.0 MB</td>" in result


def test_previewable_test(testapp):
    """Test template test."""
    file = {"type": "md"}
    template = (
        "{% if file.type is previewable %}Previewable"
        "{% else %}Not previewable{% endif %}"
    )
    assert render_template_string(template, file=file) == "Previewable"

    file["type"] = "no"
    assert render_template_string(template, file=file) == "Not previewable"

    file["type"] = "pdf"
    assert render_template_string(template, file=file) == "Previewable"

    file["type"] = ""
    assert render_template_string(template, file=file) == "Not previewable"
