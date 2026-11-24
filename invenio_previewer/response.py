# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Preview responses with a sandbox in their Content-Security-Policy header."""

from flask import current_app, make_response

from .ext import format_policy, sources_as_list
from .proxies import current_previewer


def site_content_security_policy():
    """Return the site's Content-Security-Policy as a string.

    It comes from ``APP_DEFAULT_SECURE_HEADERS`` of Invenio-App, the same
    config Talisman uses. It returns ``""`` if the site has no policy.

    For example ``"default-src 'self'; report-uri /csp-report"``.
    """
    secure_headers = current_app.config.get("APP_DEFAULT_SECURE_HEADERS", {})
    configured_policy = secure_headers.get("content_security_policy")
    if not configured_policy:
        return ""

    # Talisman accepts the policy as a string or as a dict.
    if isinstance(configured_policy, str):
        site_policy = configured_policy
    else:
        policy = {}
        for name, sources in configured_policy.items():
            policy[name] = sources_as_list(sources)
        site_policy = format_policy(policy)

    # Same as Talisman: add the report URI, if the policy doesn't have one.
    report_uri = secure_headers.get("content_security_policy_report_uri")
    if report_uri and "report-uri" not in site_policy:
        site_policy += f"; report-uri {report_uri}"

    return site_policy


def preview_response(previewer, fileobj):
    """Render a preview, with the ``sandbox`` rule in its CSP header.

    The ``sandbox`` rule only works in an HTTP header, browsers ignore it in a
    ``<meta>`` tag. But Talisman writes the CSP header after every view, and
    replaces any CSP header the view set. (Talisman is the Flask extension
    Invenio-App uses to add security headers to every response.) So:

    1. The view must turn off Talisman's CSP, with
       ``@talisman(content_security_policy={})`` from Invenio-App.
    2. The view returns this function's response. It sets the site's own
       policy again, plus ``sandbox`` if the previewer supports it.

    For example, for a sandboxed previewer the header is::

        Content-Security-Policy: default-src 'self'; sandbox allow-scripts ...
    """
    response = make_response(previewer.preview(fileobj))

    secure_headers = current_app.config.get("APP_DEFAULT_SECURE_HEADERS", {})
    report_only = secure_headers.get("content_security_policy_report_only", False)
    site_policy = site_content_security_policy()

    # The rules for the enforced header, joined with "; " at the end.
    enforced_policy = []

    if site_policy and report_only:
        # A report-only policy doesn't block anything: the browser only
        # reports what it would have blocked. The site chose that for its
        # policy, so we send it the same way.
        response.headers["Content-Security-Policy-Report-Only"] = site_policy
    elif site_policy:
        enforced_policy.append(site_policy)

    # Browsers ignore "sandbox" in a report-only header. So it always goes in
    # the enforced header (the one that blocks), even when the site's policy
    # is report-only.
    sandbox = current_previewer.sandbox_for_previewer(previewer)
    if sandbox:
        enforced_policy.append(f"sandbox {sandbox}")

    if enforced_policy:
        response.headers["Content-Security-Policy"] = "; ".join(enforced_policy)

    return response
