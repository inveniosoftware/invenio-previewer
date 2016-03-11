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

"""View method for Invenio-Records-UI for previewing files."""

from __future__ import absolute_import, print_function

import pkg_resources
from flask import Blueprint, current_app, request

try:
    pkg_resources.get_distribution('invenio-files-rest')
    HAS_FILES_REST = True
except pkg_resources.DistributionNotFound:
    HAS_FILES_REST = False


blueprint = Blueprint(
    'invenio_previewer',
    __name__,
    template_folder='templates',
    static_folder='static',
)


class PreviewFile(object):
    """Preview file default implementation."""

    def __init__(self, file, pid, record):
        """Default constructor."""
        self.file = file
        self.pid = pid
        self.record = record

    def open(self):
        """Open the file."""
        if not HAS_FILES_REST:
            raise RuntimeError(
                "Invenio-Files-REST must be installed for open to work.")

        from invenio_files_rest.models import ObjectVersion
        assert 'bucket' in self.file
        assert 'key' in self.file
        assert self.file['local']

        obj = ObjectVersion.get(self.file['bucket'], self.file['key'])
        return obj.file.storage().open()


def get_file(pid, record, filename=None):
    """Return the PreviewFile associated with the record."""
    for file in record['files']:
        if file['key'] == filename or not filename:
            return PreviewFile(file, pid, record)


def get_previewers(previewer):
    """Return available previewers ordered by PREVIEWER_PREVIEWERS_ORDER."""
    result = []

    previewers_available = {
        previewer.__name__: previewer for previewer in
        current_app.extensions['invenio-previewer'].previewers
    }

    for item in previewer or current_app.config.get(
            'PREVIEWER_PREVIEWERS_ORDER'):
        if item in previewers_available:
            result.append(previewers_available[item])

    return result


def preview(pid, record, **kwargs):
    """Preview file for given record.

    Plug this method into your ``RECORDS_UI_ENDPOINTS`` configuration:

    .. code-block:: python

        RECORDS_UI_ENDPOINTS = dict(
            recid=dict(
                # ...
                route='/records/<pid_value/preview/<filename>',
                view_imp='invenio_previewer.views.preview',
            )
        )
    """
    file = get_file(pid, record, request.args.get('filename', type=str))

    for plugin in get_previewers(previewer=[file.file.get('previewer')] if
                                 file.file.get('previewer') else None):
        if plugin.can_preview(file):
            return plugin.preview(file)
