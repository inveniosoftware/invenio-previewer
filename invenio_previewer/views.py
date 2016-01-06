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

import mimetypes
import os

from flask import Blueprint, Response, current_app, request
from invenio_documents import Document
from invenio_records import Record

blueprint = Blueprint(
    'invenio_previewer',
    __name__,
    template_folder='templates',
    static_folder='static',
)


class DocumentPreviewer(object):
    """Provides some extra information about documents."""

    def __init__(self, record_id, document):
        """Class initialization."""
        self.record_id = record_id
        self.path = os.path.dirname(document.uri)
        self.extension = document.uri[document.uri.rfind('.') + 1:]
        self.name = document.uri[
                     len(self.path) + 1: - len(self.extension) - 1]
        self.document = document

    def get_filename(self):
        """Calculate the file name."""
        return '{0}.{1}'.format(self.name, self.extension)


def get_document_previewer(record_id, filename):
    """Look for a record and return the file."""
    record = Record.get_record(record_id)

    len_documents = len(Document(record, '/files/').record['files'])

    for i_document in range(len_documents):
        document = Document(record, '/files/{0}/uri'.format(i_document))
        document_previewer = DocumentPreviewer(record_id, document)
        if not filename or document_previewer.get_filename() == filename:
            return document_previewer


def get_previewers():
    """Return available previewers ordered by PREVIEWER_PREVIEWERS_ORDER."""
    result = []
    previewers_available = {
        previewer.__name__: previewer for previewer in
        current_app.extensions['invenio-previewer'].previewers
    }

    for previewer in current_app.config.get('PREVIEWER_PREVIEWERS_ORDER'):
        if previewer in previewers_available:
            result.append(previewers_available[previewer])
    return result


@blueprint.route('/<recid>/preview', methods=['GET', 'POST'])
def preview(recid):
    """Preview file for given record."""
    document_previewer = get_document_previewer(
        recid, request.args.get('filename', type=str))

    for plugin in get_previewers():
        if plugin.can_preview(document_previewer):
            return plugin.preview(document_previewer)


@blueprint.route('/document/<recid>/<filename>')
def document(recid, filename):
    """Return a stream with the file specified in the record."""
    document_previewer = get_document_previewer(recid, filename)

    def stream_file(uri):
        with open(uri, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if chunk:
                    yield chunk
                else:
                    return
    stream = stream_file(document_previewer.document.uri)

    return Response(stream,
                    mimetype=mimetypes.guess_type(
                        document_previewer.document.uri)[0])
