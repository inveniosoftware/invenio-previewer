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
import shutil
import tempfile
import uuid
import zipfile

from flask import url_for
from invenio_db import InvenioDB, db
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records.api import Record

from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, Location, ObjectVersion


def test_view_preview_default_extension(app_assets):
    """Test view by default."""
    InvenioDB(app_assets)
    InvenioFilesREST(app_assets)
    with app_assets.test_request_context():
        with app_assets.test_client() as client:
            db.drop_all()
            db.create_all()

            # Creation of the unpreviweable file
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            file_name = 'TestDefault.def'
            filename_path = os.path.join(tmpdirname, file_name)
            with open(filename_path, 'w') as fp:
                fp.write("Empty")

            # Creation of the record and record_file
            pid_value = create_rest_files(tmpdirname, file_name, filename_path)
            db.session.commit()

            url = url_for('invenio_records_ui.recid_previewer',
                          pid_value=pid_value)
            response = client.get(url)
            assert 'we are unfortunately not' in response.data.decode(
                    'utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_markdown_extension(app_assets):
    """Test view with md files."""
    app_assets.testing = True
    InvenioDB(app_assets)
    InvenioFilesREST(app_assets)
    with app_assets.test_request_context():
        with app_assets.test_client() as client:
            db.drop_all()
            db.create_all()

            # Creation of the markdown file
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            file_name = 'markdown.md'
            filename_path = os.path.join(tmpdirname, file_name)
            with open(filename_path, 'w') as fp:
                fp.write("### Testing markdown ###")

            # Creation of the record and record_file
            pid_value = create_rest_files(tmpdirname, file_name, filename_path)
            db.session.commit()

            url = url_for('invenio_records_ui.recid_previewer',
                          pid_value=pid_value)
            response = client.get(url)
            assert '<h3>Testing markdown' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_pdf_extension(app_assets):
    """Test view with pdf files."""
    InvenioDB(app_assets)
    InvenioFilesREST(app_assets)
    with app_assets.test_request_context():
        with app_assets.test_client() as client:
            db.drop_all()
            db.create_all()

            # Creation of the pdf file
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            file_name = 'pdf.pdf'
            filename_path = os.path.join(tmpdirname, file_name)
            with open(filename_path, 'w') as fp:
                fp.write("Empty")

            # Creation of the record and record_file
            pid_value = create_rest_files(tmpdirname, file_name, filename_path)
            db.session.commit()

            url = url_for('invenio_records_ui.recid_previewer',
                          pid_value=pid_value)
            response = client.get(url)
            assert 'PDFView.open(\'' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_csv_dthreejs_extension(app_assets):
    """Test view with csv files."""
    InvenioDB(app_assets)
    InvenioFilesREST(app_assets)
    with app_assets.test_request_context():
        with app_assets.test_client() as client:
            db.drop_all()
            db.create_all()

            # Creation of the csv file
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            file_name = 'comma.csv'
            filename_path = os.path.join(tmpdirname, file_name)
            with open(filename_path, 'w') as fp:
                fp.write("A,B\n1,2")

            # Creation of the record and record_file
            pid_value = create_rest_files(tmpdirname, file_name, filename_path)
            db.session.commit()

            url = url_for('invenio_records_ui.recid_previewer',
                          pid_value=pid_value)
            response = client.get(url)
            assert 'data-csv-source="' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def test_view_preview_zip_extension(app_assets):
    """Test view with zip files."""
    InvenioDB(app_assets)
    InvenioFilesREST(app_assets)
    with app_assets.test_request_context():
        with app_assets.test_client() as client:
            db.drop_all()
            db.create_all()

            # Creation of the zip file
            tmpdirname = tempfile.mktemp()
            if not os.path.exists(tmpdirname):
                os.makedirs(tmpdirname)
            file_name = 'zipfile.zip'
            filename_path = os.path.join(tmpdirname, file_name)
            zipf = zipfile.ZipFile(filename_path, 'w')
            zipf.writestr('Example.txt', 'This is an example')
            zipf.close()

            # Creation of the record and record_file
            pid_value = create_rest_files(tmpdirname, file_name, filename_path)
            db.session.commit()

            url = url_for('invenio_records_ui.recid_previewer',
                          pid_value=pid_value)
            response = client.get(url)
            assert 'Example.txt' in response.data.decode('utf-8')
            shutil.rmtree(tmpdirname)


def create_rest_files(tmpdirname, file_name, filename_path):
    """Create a file with the file and its content."""
    rec_uuid = uuid.uuid4()
    provider = RecordIdProvider.create(object_type='rec',
                                       object_uuid=rec_uuid)
    pid_value = provider.pid.pid_value
    with db.session.begin_nested():
        loc = Location(name='local', uri=tmpdirname, default=True)
    with db.session.begin_nested():
        bucket = Bucket.create(loc)
        with open(filename_path, 'rb') as fp:
            ObjectVersion.create(bucket, file_name, stream=fp)
        Record.create({
            "pid_value": pid_value,
            "title": "TestDefault",
            "files": [
                {
                    "uri": '/files/{0}/{1}'.format(str(bucket.id),
                                                   file_name),
                    'bucket': str(bucket.id),
                    'key': file_name,
                    'local': True
                }
            ]
        }, id_=rec_uuid)
    return pid_value
