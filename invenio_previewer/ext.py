# SPDX-FileCopyrightText: 2016-2026 CERN.
# SPDX-FileCopyrightText: 2025 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module for previewing files."""

from os.path import splitext
from urllib.parse import urlsplit

from flask import current_app
from invenio_base.utils import entry_points
from werkzeug.utils import cached_property, import_string

from . import config
from .extensions import default as default_previewer
from .views import blueprint


def obj_or_import_string(value, default=None):
    """Import string or return object."""
    if isinstance(value, str):
        return import_string(value)
    elif value:
        return value
    return default


def load_or_import_from_config(key, app=None, default=None):
    """Load or import value from config."""
    app = app or current_app
    imp = app.config.get(key)
    return obj_or_import_string(imp, default=default)


# A Content-Security-Policy is a list of rules called "directives". Each one
# says where the page can load one kind of thing from. For example
# "script-src 'self'" means scripts can only come from our own site.
#
# Previewers load the file they show with two of these directives:
# - connect-src: used when JavaScript downloads the file. The PDF, CSV and
#   GeoJSON previewers do this.
# - media-src: used by the <audio> and <video> players.
#
# We add external domains only to these two, and never to script-src. So a
# file from S3 can be shown or played, but never run as a script.
FILE_LOADING_DIRECTIVES = ["connect-src", "media-src"]


def sources_as_list(sources):
    """Return the sources of a directive as a list.

    Sources can be configured as a list, like ``["'self'", "data:"]``, or as a
    string with spaces, like ``"'self' data:"``.
    """
    if not sources:
        return []
    if isinstance(sources, str):
        return sources.split()
    return list(sources)


def domain_of_url(url):
    """Return the domain of a URL, with its scheme and port but no path.

    For example ``https://s3.example.org:9000/bucket`` becomes
    ``https://s3.example.org:9000``. This is the format CSP needs.
    """
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


def format_policy(policy):
    """Turn a policy dict into a string, like ``"default-src 'self'; ..."``."""
    directives = []
    for name, sources in policy.items():
        directive = " ".join([name] + sources)
        directives.append(directive)
    return "; ".join(directives)


class _InvenioPreviewerState(object):
    """State object."""

    def __init__(self, app, entry_point_group=None):
        """Initialize state."""
        self.app = app
        self.entry_point_group = entry_point_group
        self.previewers = {}
        self._previewable_extensions = set()
        self._container_item_previewable_extensions = set()

    @cached_property
    def previewable_extensions(self):
        """Return previewable extensions for files."""
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None
        return self._previewable_extensions

    @cached_property
    def container_item_previewable_extensions(self):
        """Return previewable extensions for container items."""
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None
        return self._container_item_previewable_extensions

    @cached_property
    def previewer_preference(self):
        """Get previewer preference from config."""
        return self.app.config.get("PREVIEWER_PREFERENCE", [])

    @cached_property
    def previewer_container_item_preference(self):
        """Get container previewer preference from config."""
        return (
            self.app.config.get("PREVIEWER_CONTAINER_ITEM_PREFERENCE", [])
            or self.previewer_preference
        )

    @cached_property
    def record_file_factory(self):
        """Load default record file factory."""
        try:
            from invenio_records_files.utils import record_file_factory

            default = record_file_factory
        except ImportError:

            def default(pid, record, filename):
                return None

        return load_or_import_from_config(
            "PREVIEWER_RECORD_FILE_FACOTRY",
            app=self.app,
            default=default,
        )

    @property
    def css_bundles(self):
        return self.app.config["PREVIEWER_BASE_CSS_BUNDLES"]

    @property
    def js_bundles(self):
        return self.app.config["PREVIEWER_BASE_JS_BUNDLES"]

    @property
    def content_security_policy(self):
        """Return the Content-Security-Policy of previews as a string.

        It is ``PREVIEWER_CONTENT_SECURITY_POLICY`` plus the external domains
        files are downloaded from, like an S3 storage. It returns an empty
        string if the policy is disabled.

        For example, with ``PREVIEWER_EXTERNAL_DOMAINS = ["https://s3.example.org"]``
        and the default policy, it returns (one line, split here to read it)::

            default-src 'self';
            script-src 'self';
            style-src 'self' 'unsafe-inline';
            img-src * data: blob:;
            font-src 'self' data:;
            connect-src 'self' https://s3.example.org;
            media-src 'self' blob: https://s3.example.org;
            worker-src 'self' blob:;
            object-src 'none';
            base-uri 'none';
            form-action 'self'

        Only ``connect-src`` and ``media-src`` get the S3 domain.
        """
        configured_policy = self.app.config.get("PREVIEWER_CONTENT_SECURITY_POLICY")
        if not configured_policy:
            return ""

        policy = {}
        for name, sources in configured_policy.items():
            policy[name] = sources_as_list(sources)

        external_domains = self.external_file_domains
        if external_domains:
            self._allow_file_loading_from(policy, external_domains)

        return format_policy(policy)

    @property
    def external_file_domains(self):
        """Return the external domains that files are downloaded from.

        When files are stored in S3, downloading a file redirects the browser to
        a link on the S3 domain. If the previews' policy does not allow that
        domain, the browser blocks the file.
        """
        domains = sources_as_list(self.app.config.get("PREVIEWER_EXTERNAL_DOMAINS"))

        # This Invenio-S3 setting is only set for S3 servers that are not AWS,
        # for example MinIO or Ceph.
        s3_endpoint_url = self.app.config.get("S3_ENDPOINT_URL")
        if s3_endpoint_url:
            s3_domain = domain_of_url(s3_endpoint_url)
            if s3_domain not in domains:
                domains.append(s3_domain)

        return domains

    def _allow_file_loading_from(self, policy, domains):
        """Add the domains to connect-src and media-src of the policy.

        Changes ``policy`` directly.
        """
        for name in FILE_LOADING_DIRECTIVES:
            if name in policy:
                sources = policy[name]

            elif "default-src" in policy:
                # When a directive is missing, the browser uses default-src
                # instead. So we start from a copy of default-src, to keep
                # allowing what it allows. We drop "'none'", because it can't
                # be mixed with other sources.
                sources = []
                for source in policy["default-src"]:
                    if source != "'none'":
                        sources.append(source)

            else:
                # The directive and default-src are both missing, so the
                # browser already allows any domain. Adding the directive
                # would only block more, so we leave it out.
                continue

            policy[name] = sources + domains

    def find_previewer_for_file_name(self, filename, previewer_name=None):
        """Guess which previewer will show a file, using only its name.

        :param filename: The file's name, for example ``"report.pdf"``.
        :param previewer_name: The previewer set in the file's metadata, if
            any. It wins over the guess from the file's extension.
        :returns: A previewer. The default previewer if no other one matches.
        """
        self._load_previewers()

        if previewer_name and previewer_name in self.previewers:
            return self.previewers[previewer_name]

        extension = splitext(filename)[1]  # "report.PDF" -> ".PDF"
        extension = extension.lstrip(".").lower()  # ".PDF" -> "pdf"

        # Same order as the preview view: PREVIEWER_PREFERENCE.
        for previewer in self.iter_previewers():
            extensions = getattr(previewer, "previewable_extensions", [])
            if extension in extensions:
                return previewer

        return default_previewer

    def sandbox_for_previewer(self, previewer):
        """Return the sandbox for a previewer's previews, or ``""`` for none.

        For example ``"allow-scripts allow-popups"``, which is the value of
        ``PREVIEWER_SANDBOX``.
        """
        sandbox = self.app.config.get("PREVIEWER_SANDBOX")
        if not sandbox:
            return ""

        # "sandbox" is optional, previewers without it are not sandboxed.
        previewer_supports_sandbox = getattr(previewer, "sandbox", False)
        if not previewer_supports_sandbox:
            return ""

        return sandbox

    def register_previewer(self, name, previewer):
        """Register a previewer in the system."""
        if name in self.previewers:
            if self.previewers[name] is previewer:
                return
            else:
                raise RuntimeError(
                    f"Previewer '{name}' is already registered with instance "
                    f"{self.previewers[name]!r}, cannot register different instance "
                    f"{previewer!r}."
                )
        self.previewers[name] = previewer
        if hasattr(previewer, "previewable_extensions"):
            # Add the extension only if the previewer is in the preference list (it is enabled).
            if name in self.previewer_preference:
                self._previewable_extensions |= set(previewer.previewable_extensions)
            if name in self.previewer_container_item_preference:
                self._container_item_previewable_extensions |= set(
                    previewer.previewable_extensions
                )

    def load_entry_point_group(self, entry_point_group):
        """Load previewers from an entry point group."""
        for ep in entry_points(group=entry_point_group):
            self.register_previewer(ep.name, ep.load())

    def _load_previewers(self):
        """Load the previewers from their entry points, only the first time."""
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None

    def iter_previewers(self, previewers=None):
        """Get the previewers in the order of ``previewers``.

        By default, in the order of the ``PREVIEWER_PREFERENCE`` setting.
        """
        self._load_previewers()

        previewers = previewers or self.previewer_preference

        for item in previewers:
            if item in self.previewers:
                yield self.previewers[item]

    def iter_container_item_previewers(self, previewers=None):
        """Get previewers ordered by PREVIEWER_CONTAINER_ITEM_PREFERENCE."""
        return self.iter_previewers(
            previewers=previewers or self.previewer_container_item_preference
        )


class InvenioPreviewer(object):
    """Invenio-Previewer extension."""

    def __init__(self, app, **kwargs):
        """Extension initialization."""
        if app:
            self._state = self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group="invenio_previewer.previewers"):
        """Flask application initialization."""
        self.init_config(app)
        app.register_blueprint(blueprint)
        state = _InvenioPreviewerState(app, entry_point_group=entry_point_group)
        app.extensions["invenio-previewer"] = state
        return state

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault("PREVIEWER_BASE_TEMPLATE", "invenio_previewer/base.html")

        for k in dir(config):
            if k.startswith("PREVIEWER_"):
                app.config.setdefault(k, getattr(config, k))

    def __getattr__(self, name):
        """Proxy to state object."""
        return getattr(self._state, name, None)
