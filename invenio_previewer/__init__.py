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

r"""Invenio module for previewing files.

Invenio-Records-UI is a core component of Invenio which provides configurable
extensions to preview files in a web browser. It uses Invenio-Records to get the
information about the file to preview and it is using some third-party modules
that provide some extra funcionality.

Initialization
--------------
First create a Flask application (Flask-CLI is not needed for Flask
version 1.0+):

>>> from flask import Flask
>>> from flask_cli import FlaskCLI
>>> app = Flask('myapp')
>>> app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
>>> ext_cli = FlaskCLI(app)

You initialize Records-Previewer like a normal Flask extension, however
Invenio-Records-UI is dependent on Invenio-Records-UI and Invenio-files-REST,
so you need to initialize these extensions and its dependencies first:

>>> from flask_babelex import Babel
>>> ext_babel = Babel(app)
>>> from invenio_db import InvenioDB, db
>>> ext_db = InvenioDB(app)
>>> from invenio_assets import InvenioAssets
>>> ext_assets = InvenioAssets(app)
>>> from invenio_access import InvenioAccess
>>> from invenio_accounts import InvenioAccounts
>>> ext_accounts = InvenioAccounts(app)
>>> ext_access = InvenioAccess(app)
>>> from invenio_records import InvenioRecords
>>> from invenio_records_ui import InvenioRecordsUI
>>> ext_records = InvenioRecords(app)
>>> ext_records_ui = InvenioRecordsUI(app)
>>> from invenio_files_rest import InvenioFilesREST
>>> ext_files_rest = InvenioFilesREST(app)
>>> from invenio_previewer import InvenioPreviewer
>>> ext_previewer = InvenioPreviewer(app)

Configuring Records-UI
----------------------
We need to configure Records-UI since the endpoint for the previewer is declared
here. Let's map the route ``/records/<pid_value>/preview`` which shows us the
preview of the file in our browser.

>>> app.config.update(
...     SECRET_KEY='CHANGEME',
...     RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
...     REST_ENABLE_CORS=True,
...     RECORDS_UI_ENDPOINTS=dict(
...         recid=dict(
...             pid_type='recid',
...             route='/records/<pid_value>',
...             template='invenio_records_ui/detail.html',
...         ),
...         recid_previewer=dict(
...             pid_type='recid',
...             route='/records/<pid_value>/preview',
...             view_imp='invenio_previewer.views:preview',
...         ),
...     )
... )

Previewing a file
-----------------
Before we can display a document, we need to create a bucket and a record
storing some information about the file. We need also to create a PID for the
record:

First of all, lets create the uuid and the PID provider:
>>> from uuid import uuid4
>>> from invenio_pidstore.providers.recordid import RecordIdProvider
>>> recid = uuid4()
>>> provider = RecordIdProvider.create(object_type='rec', object_uuid=recid)

Now, we are going to create the bucket and store the file inside:
>>> from invenio_files_rest.models import Bucket, Location, ObjectVersion
>>> file_name = 'markdown.md'
>>> bucket = Bucket.create(loc)
>>> loc = Location(name='local', uri=data_path, default=True)
>>> db.session.commit()
>>> ObjectVersion.create(bucket, file_name, stream=stream)

Let's create the record with the file information:
>>> from invenio_records import Record
>>> data = {
...     'pid_value': provider.pid.pid_value,
...     'files': [
...         {
...             'uri': '/files/{0}/{1}'.format(str(bucket.id), file_name),
...             'key': file_name,
...             'bucket': str(bucket.id),
...             'local': True,
...         }
...     ]
... }
>>> Record.create(data, id_=recid)
>>> db.session.commit()

We should be able to see now the result HTML generated from the markdown file:
>>> with app.test_client() as client:
...     res = client.get('/records/1/preview')
>>> res.data


Bundled previewers
------------------

This module contains several previewers out of the box:

- Markdown: Previews a markdown file. It is based on python ``mistune`` library.

- ``CSV`` - Previews ``comma separated values`` files but it can actually works
  with any other tabular data format in plain text based on the idea of
  separated values due to it is detecting the delimiter between the characters
  automatically. On the client side, the file is previewed using ``D3JS``
  library.

- ``PDF`` - Previews a ``portable document format`` file in your browser using
  ``PDFJS`` library.

- ``ZIP`` - Previews file tree inside the archive. You can specify a files limit
  to avoid a temporary lock in both of client and server side when you are dealing
  with large ZIP files. By default, this limit is set 1000 files.

- ``Default`` - This previewer is intended to be a fallback previewer to those
  cases when there is no previewer to deal with some file type. It is showing a
  simple message.

Local vs. remote files
----------------------

Some of the extensions are only working with local files. This is the case of
CSV, Markdown and ZIP previewers. A file is considered local if it is stored in
Invenio-Files-REST. However, the PDF previewer doesn't need have the files
stored locally.

Behind this behaviour there are only security reasons: The server needs to open
and process the file.

Override default previewers
---------------------------

- ``PREVIEWER_PREVIEWERS_ORDER`` - Contains a list of string which specify the
  order of the previewers. The first item in the list is the most prioritized
  previewer in case of collision. It is a good practise to use a fallback
  previewer (i.e. ``default`` previwer) which can works with all file types,
  otherwise, the system returns a 500 HTTP error code. The system is going to
  use only, and only only the previewers that are listed in this variable.

Custom previewer
----------------
The implementation of a custom preview is an easy process which do not require
to have a deep acknowledgment about the Invenio architecture.

Basically you only need to write two methods and declare the entry point and the
priority of your previewer.

We are going to instantiate the process creating a TXT previewer:

Implementation:
We need to create the Python module which is going to contain the
``can_preview`` and ``preview`` methods. Both of them expect a ``PreviewFile``
object (You can see the implementation of this file on
``invenio_previewer.views`` module). As you are probably guessing,
the ``can_preview`` method should return a boolean specifying if the previewer
can shows the file.

In the case of the ``preview`` method, what you should return is a Flask HTTP
response so we can return also a simple string.

For our TXT previewer, we can create a file with the following content:

>>> def can_preview(file):
...     return file.file['uri'].endswith('.txt')

>>> def preview(file):
...     fp = file.open()
...     content = fp.read().decode('utf-8')
...     fp.close()
...     return content

Configuration:
Once we have our code, we should register our previewer in the previwer entry
point. So, go to your ``setup.py`` and create a new entry (If it doesn't exist)
to declare ``invenio_previewer.previewers`` entry points. Then, you should add
a new entry with specifying the python path of your module:
>>> 'invenio_previewer.previewers': [
>>>     'tex_previewer = myproject.modules.previewer.extensions.txt_previewer',
>>> ]

The configuration above made it is only making to our project to be aware of the
module but the previewer can not be used. As we said before, you need to add it
to ``PREVIEWER_PREVIEWERS_ORDER`` in the correct position. The first position
is going to be perfect in the case of this TXT previewer:
>>> PREVIEWER_PREVIEWERS_ORDER=
>>>     [
>>>         'invenio_previewer.extensions.csv_dthreejs',
>>>         'invenio_previewer.extensions.mistune',
>>>         'invenio_previewer.extensions.pdfjs',
>>>         'invenio_previewer.extensions.zip',
>>>         'invenio_previewer.extensions.default',
>>>     ]

Now, the previewer is ready to be used.

Bundles:
In the previously described previewer, we were returning a simple string as
response  but a real implementation should return a HTML. This HTML should
extends ``invenio_previewer/abstract_previewer.html`` in order to take advantage
of many presentation features.

But when you are defining a new template, maybe you are requiring some files
like javascript or style documents. For those cases, you need to create a
bundle. Check ``Invenio-Assets`` out to learn how to add them.
"""

from __future__ import absolute_import, print_function

from .ext import InvenioPreviewer
from .version import __version__

__all__ = ('__version__', 'InvenioPreviewer')
