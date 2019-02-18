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

r"""Minimal Flask application example for development.

1. Setup the application and create demo data:

.. code-block:: console

   $ cd examples
   $ ./app-setup.py

2. Our record with pid 1 contains several files. You can check out the
different types of files by changing the filename in the url
to one of the following values: markdown.md, csvfile.csv, zipfile.zip,
jsonfile.json, xmlfile.xml, notebook.ipynb, jpgfile.jpg, pngfile.png

`http://localhost:5000/records/1/preview?filename=csvfile.csv`
"""

from __future__ import absolute_import, print_function

import os
from uuid import uuid4

from flask import Flask
from flask_babelex import Babel
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, Location
from invenio_i18n import InvenioI18N
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records import InvenioRecords
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets
from invenio_records_ui import InvenioRecordsUI
from invenio_records_ui.views import create_blueprint_from_app

from invenio_previewer import InvenioPreviewer

# Create Flask application
app = Flask(__name__)
app.config.update(
    SECRET_KEY='CHANGEME',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
    RECORDS_UI_ENDPOINTS=dict(
        recid=dict(
            pid_type='recid',
            route='/records/<pid_value>',
            template='invenio_records_ui/detail.html',
        ),
        recid_files=dict(
            pid_type='recid',
            route='/records/<pid_value>/files/<filename>',
            view_imp='invenio_records_files.utils:file_download_ui',
            record_class='invenio_records_files.api:Record',
        ),
        recid_previewer=dict(
            pid_type='recid',
            route='/records/<pid_value>/preview',
            view_imp='invenio_previewer.views:preview',
            record_class='invenio_records_files.api:Record',
        )
    )
)
Babel(app)
InvenioI18N(app)
InvenioDB(app)
InvenioAssets(app)
InvenioRecords(app)
InvenioFilesREST(app)
InvenioPreviewer(app)
InvenioRecordsUI(app)
app.register_blueprint(create_blueprint_from_app(app))


@app.cli.command()
def fixtures():
    """Command for working with test data."""
    temp_path = os.path.join(os.path.dirname(__file__), 'temp')
    demo_files_path = os.path.join(os.path.dirname(__file__), 'demo_files')

    # Create location
    loc = Location(name='local', uri=temp_path, default=True)
    db.session.add(loc)
    db.session.commit()

    # Example files from the data folder
    demo_files = (
        'markdown.md',
        'csvfile.csv',
        'zipfile.zip',
        'jsonfile.json',
        'xmlfile.xml',
        'notebook.ipynb',
        'jpgfile.jpg',
        'pngfile.png',
    )

    rec_uuid = uuid4()
    provider = RecordIdProvider.create(object_type='rec', object_uuid=rec_uuid)
    data = {
        'pid_value': provider.pid.pid_value,
    }

    record = Record.create(data, id_=rec_uuid)
    bucket = Bucket.create()
    RecordsBuckets.create(record=record.model, bucket=bucket)

    # Add files to the record
    for f in demo_files:
        with open(os.path.join(demo_files_path, f), 'rb') as fp:
            record.files[f] = fp

    record.files.flush()
    record.commit()
    db.session.commit()
