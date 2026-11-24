# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Tests for sandboxing previews."""

from types import SimpleNamespace

import pytest
from flask import render_template_string
from mock import patch

from invenio_previewer.extensions import default as default_previewer
from invenio_previewer.response import preview_response

SANDBOX = "allow-scripts allow-popups allow-popups-to-escape-sandbox"


def fake_previewer(sandbox):
    """Return a previewer that renders a fixed page."""
    return SimpleNamespace(sandbox=sandbox, preview=lambda fileobj: "<p>preview</p>")


@pytest.mark.parametrize(
    "filename, previewer_name, expected",
    [
        ("notes.txt", None, "txt"),
        ("NOTES.TXT", None, "txt"),
        ("report.pdf", None, "pdfjs"),
        # the previewer set in the file's metadata wins over the extension
        ("report.pdf", "txt", "txt"),
        ("notes.txt", "pdfjs", "pdfjs"),
        # an unknown previewer name falls back to the extension
        ("notes.txt", "does-not-exist", "txt"),
    ],
)
def test_find_previewer_for_file_name(testapp, filename, previewer_name, expected):
    """Test the guess of the previewer from the file name."""
    state = testapp.extensions["invenio-previewer"]
    previewer = state.find_previewer_for_file_name(filename, previewer_name)
    assert previewer is state.previewers[expected]


def test_find_previewer_for_file_name_default(testapp):
    """Test that files without a matching previewer get the default one."""
    state = testapp.extensions["invenio-previewer"]
    previewer = state.find_previewer_for_file_name("data.unknown-extension")
    assert previewer is default_previewer


def test_sandbox_for_previewer(testapp):
    """Test that only previewers with ``sandbox = True`` are sandboxed."""
    state = testapp.extensions["invenio-previewer"]
    assert state.sandbox_for_previewer(fake_previewer(sandbox=True)) == SANDBOX
    assert state.sandbox_for_previewer(fake_previewer(sandbox=False)) == ""
    assert state.sandbox_for_previewer(SimpleNamespace()) == ""

    with patch.dict(testapp.config, {"PREVIEWER_SANDBOX": None}):
        assert state.sandbox_for_previewer(fake_previewer(sandbox=True)) == ""


def test_iframe_sandbox_template_function(testapp):
    """Test the template function for the preview iframe."""
    template = "{{ previewer_iframe_sandbox(filename) }}"
    with testapp.test_request_context():
        # the text previewer has sandbox = True, PDF.js doesn't
        assert render_template_string(template, filename="notes.txt") == SANDBOX
        assert render_template_string(template, filename="report.pdf") == ""


def test_preview_file_macro_sandbox(testapp):
    """Test that the preview_file macro adds the sandbox to the iframe."""
    template = """
        {%- from "invenio_previewer/macros.html" import preview_file -%}
        {{ preview_file("invenio_records_ui.recid_previewer", pid, filename) }}
    """
    pid = SimpleNamespace(pid_value="1")
    with testapp.test_request_context():
        sandboxed = render_template_string(template, pid=pid, filename="notes.txt")
        not_sandboxed = render_template_string(template, pid=pid, filename="a.pdf")
    assert f'sandbox="{SANDBOX}"' in sandboxed
    assert "sandbox=" not in not_sandboxed


SITE_HEADERS = {
    "content_security_policy": {"default-src": ["'self'"], "img-src": "* data:"},
    "content_security_policy_report_uri": None,
    "content_security_policy_report_only": False,
}


def get_preview_headers(testapp, previewer, secure_headers):
    """Return the headers of a preview response."""
    config = {"APP_DEFAULT_SECURE_HEADERS": secure_headers}
    with patch.dict(testapp.config, config), testapp.test_request_context():
        response = preview_response(previewer, fileobj=None)
    return response.headers


def test_preview_response_sandboxed(testapp):
    """Test that the site's policy is kept and sandbox is added."""
    headers = get_preview_headers(testapp, fake_previewer(True), SITE_HEADERS)
    assert headers["Content-Security-Policy"] == (
        f"default-src 'self'; img-src * data:; sandbox {SANDBOX}"
    )
    assert "Content-Security-Policy-Report-Only" not in headers


def test_preview_response_not_sandboxed(testapp):
    """Test that previewers without sandbox only get the site's policy."""
    headers = get_preview_headers(testapp, fake_previewer(False), SITE_HEADERS)
    assert headers["Content-Security-Policy"] == "default-src 'self'; img-src * data:"


def test_preview_response_report_uri(testapp):
    """Test that the site's report URI is kept, like Talisman does."""
    secure_headers = {**SITE_HEADERS, "content_security_policy_report_uri": "/r"}
    headers = get_preview_headers(testapp, fake_previewer(False), secure_headers)
    assert headers["Content-Security-Policy"].endswith("; report-uri /r")


def test_preview_response_report_only(testapp):
    """Test that sandbox is enforced even if the site's policy is report-only."""
    secure_headers = {**SITE_HEADERS, "content_security_policy_report_only": True}
    headers = get_preview_headers(testapp, fake_previewer(True), secure_headers)
    assert headers["Content-Security-Policy-Report-Only"] == (
        "default-src 'self'; img-src * data:"
    )
    assert headers["Content-Security-Policy"] == f"sandbox {SANDBOX}"


def test_preview_response_no_site_policy(testapp):
    """Test previews of sites without a policy."""
    secure_headers = {"content_security_policy": None}
    sandboxed = get_preview_headers(testapp, fake_previewer(True), secure_headers)
    assert sandboxed["Content-Security-Policy"] == f"sandbox {SANDBOX}"

    plain = get_preview_headers(testapp, fake_previewer(False), secure_headers)
    assert "Content-Security-Policy" not in plain


def test_preview_response_string_site_policy(testapp):
    """Test that the site's policy can be a string, like Talisman allows."""
    secure_headers = {"content_security_policy": "default-src 'self'"}
    headers = get_preview_headers(testapp, fake_previewer(True), secure_headers)
    assert headers["Content-Security-Policy"] == (
        f"default-src 'self'; sandbox {SANDBOX}"
    )
