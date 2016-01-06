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


"""Views module tests."""

from __future__ import absolute_import, print_function

import os
import random
import shutil
import string
import tempfile
import uuid
import zipfile

from flask import url_for
from invenio_db import db
from invenio_records.api import Record


def test_view_preview_default_extension(app_assets_db):
    """Test view by default."""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": "/tmp/TestDefault.def"}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.preview', recid=rec_uuid)
            response = client.get(url)
            assert 'we are unfortunately not' in response.data.decode('utf-8')


def test_view_preview_markdown_extension(app_assets_db):
    """Test view with md files."""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            filename_path = os.path.join(tmpdirname, 'markdown.md')
            with open(filename_path, 'w') as file:
                file.write("### Testing markdown ###")

            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": filename_path}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.preview', recid=rec_uuid)
            response = client.get(url)
            assert '<h3>Testing markdown' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_pdf_extension(app_assets_db):
    """Test view with pdf files."""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            filename_path = os.path.join(tmpdirname, 'pdf.pdf')

            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": filename_path}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.preview', recid=rec_uuid)
            response = client.get(url)
            assert 'PDFView.open(\'' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_csv_dthreejs_extension(app_assets_db):
    """Test view with csv files."""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            filename_path = os.path.join(tmpdirname, 'comma.csv')
            with open(filename_path, 'w') as file:
                file.write("A,B\n1,2")

            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": filename_path}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.preview', recid=rec_uuid)
            response = client.get(url)
            assert 'data-csv-source="' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_zip_extension(app_assets_db):
    """Test view with zip files."""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            filename_path = os.path.join(tmpdirname, 'zipfile.zip')
            zipf = zipfile.ZipFile(filename_path, 'w')
            zipf.writestr('Example.txt', 'This is an example')
            zipf.close()

            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": filename_path}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.preview', recid=rec_uuid)
            response = client.get(url)
            assert 'Example.txt' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_documents(app_assets_db):
    """Test the view invenio_previewer.document"""
    with app_assets_db.test_request_context():
        with app_assets_db.test_client() as client:
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            content = ''.join(random.choice(string.ascii_letters)
                              for i in range(16536))

            filename = 'file.txt'
            filename_path = os.path.join(tmpdirname, filename)
            with open(filename_path, 'w') as file:
                file.write(content)

            rec_uuid = uuid.uuid4()
            with db.session.begin_nested():
                Record.create({
                    "title": "TestDefault",
                    "files": [{"uri": filename_path}]
                }, id_=rec_uuid)
            url = url_for('invenio_previewer.document',
                          recid=rec_uuid, filename=filename)
            response = client.get(url)
            assert content == response.data.decode('ascii')
            shutil.rmtree(tmpdirname)
