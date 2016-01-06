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

from .views import blueprint


class InvenioPreviewer(object):
    """Invenio-Previewer extension."""

    def __init__(self, app, **kwargs):
        """Extension initialization."""
        self.previewers = []
        self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_previewer.previewers'):
        """Flask application initialization."""
        self.init_config(app)
        app.register_blueprint(blueprint)
        if entry_point_group:
            self.load_entry_point_group(entry_point_group)

        app.extensions['invenio-previewer'] = self

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            'PREVIEWER_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_previewer/base.html'))
        app.config.setdefault(
            'PREVIEWER_ABSTRACT_TEMPLATE',
            'invenio_previewer/abstract_previewer.html')

        app.config.setdefault(
            'PREVIEWER_PREVIEWERS_ORDER',
            [
                'invenio_previewer.previewerext.csv_dthreejs',
                'invenio_previewer.previewerext.mistune',
                'invenio_previewer.previewerext.pdfjs',
                'invenio_previewer.previewerext.zip',
                'invenio_previewer.previewerext.default',
            ]
        )

    def register_previewer(self, previewer):
        """Register a previewer in the system."""
        if previewer not in self.previewers:
            self.previewers.append(previewer)

    def load_entry_point_group(self, entry_point_group):
        """Load previewers from an entry point group."""
        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            self.register_previewer(ep.load())
