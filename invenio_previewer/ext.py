# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module for previewing files."""

from __future__ import absolute_import, print_function

import pkg_resources
from werkzeug.utils import cached_property

from . import config
from .views import blueprint


class _InvenioPreviewerState(object):
    """State object."""

    def __init__(self, app, entry_point_group=None):
        """Initialize state."""
        self.app = app
        self.entry_point_group = entry_point_group
        self.previewers = {}
        self._previewable_extensions = set()

    @cached_property
    def previewable_extensions(self):
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None
        return self._previewable_extensions

    @property
    def css_bundles(self):
        return self.app.config['PREVIEWER_BASE_CSS_BUNDLES']

    @property
    def js_bundles(self):
        return self.app.config['PREVIEWER_BASE_JS_BUNDLES']

    def register_previewer(self, name, previewer):
        """Register a previewer in the system."""
        if name in self.previewers:
            assert name not in self.previewers, \
                "Previewer with same name already registered"
        self.previewers[name] = previewer
        if hasattr(previewer, 'previewable_extensions'):
            self._previewable_extensions |= set(
                    previewer.previewable_extensions)

    def load_entry_point_group(self, entry_point_group):
        """Load previewers from an entry point group."""
        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            self.register_previewer(ep.name, ep.load())

    def iter_previewers(self, previewers=None):
        """Get previewers ordered by PREVIEWER_PREVIEWERS_ORDER."""
        if self.entry_point_group is not None:
            self.load_entry_point_group(self.entry_point_group)
            self.entry_point_group = None

        previewers = previewers or \
            self.app.config.get('PREVIEWER_PREFERENCE', [])

        for item in previewers:
            if item in self.previewers:
                yield self.previewers[item]


class InvenioPreviewer(object):
    """Invenio-Previewer extension."""

    def __init__(self, app, **kwargs):
        """Extension initialization."""
        if app:
            self._state = self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_previewer.previewers'):
        """Flask application initialization."""
        self.init_config(app)
        app.register_blueprint(blueprint)
        state = _InvenioPreviewerState(
            app,
            entry_point_group=entry_point_group)
        app.extensions['invenio-previewer'] = state
        return state

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            'PREVIEWER_BASE_TEMPLATE', 'invenio_previewer/base.html')

        for k in dir(config):
            if k.startswith('PREVIEWER_'):
                app.config.setdefault(k, getattr(config, k))

    def __getattr__(self, name):
        """Proxy to state object."""
        return getattr(self._state, name, None)
