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


"""Minimal Flask application example for development.


1. Create the database and the tables:

.. code-block:: console

    $ cd examples
    $ flask -a app.py db init
    $ flask -a app.py db create


2. Collect npm, requirements from registered bundles:

.. code-block:: console
    $ flask -a app.py npm


3. Install the npm packages:

.. code-block:: console
    $ cd static
    $ npm install
    $ cd ..


3. Copy the static files from the Python packages into the Flask
application's static folder:

.. code-block:: console
    $ flask -a app.py collect -v


4. Build the assets as they are defined in bundle.py:

.. code-block:: console
    $ flask -a app.py assets build


5. Creation of files of several types, their records and the insertion in our
application. Grab the last line printed in the terminal after each insertion
because it is the identifier of the records which is needed in order to
be able to preview the files:

5.1. A Markdown file:

.. code-block:: console

    $ echo '## This is Markdown' > /tmp/markdown.md
    $ echo '{"title": "TestMaDF", "files": [{"uri": "/tmp/markdown.md"}]}' \
      > markdown.json
    $ flask -a app.py records create < markdown.json


5.2. A CSV file:

.. code-block:: console

    $ echo $'A,B\n1,1\n2,4\n3,9' > /tmp/square.csv
    $ echo '{"title": "TestCSV", "files": [{"uri": "/tmp/square.csv"}]}' \
      > csv.json
    $ flask -a app.py records create < csv.json


5.3. A PDF file:

.. code-block:: console

    $ wget http://stlab.adobe.com/wiki/images/d/d3/Test.pdf -O /tmp/pdfile.pdf
    $ echo '{"title": "TestPDF", "files": [{"uri": "/tmp/pdfile.pdf"}]}' \
      > pdf.json
    $ flask -a app.py records create < pdf.json


5.4. A ZIP file containing all the previous files:

.. code-block:: console

    $ zip -r /tmp/zipfile.zip /tmp/pdfile.pdf /tmp/markdown.md /tmp/square.csv
    $ echo '{"title": "TestZip", "files": [{"uri": "/tmp/zipfile.zip"}]}' \
      > zip.json
    $ flask -a app.py records create < zip.json


5.5. And a record composed by separated files:

.. code-block:: console

    $ echo '{"title": "TestZip", "files":
      [{"uri":"/tmp/square.csv"},{"uri": "/tmp/pdfile.pdf"}]}' > multiple.json
    $ flask -a app.py records create < multiple.json

6. Run the test server:

.. code-block:: console
    $ flask -a app.py --debug run

7. Open a web browser and enter to the url
`http://localhost:5000/RECORD_ID/preview` where
`RECORD_ID` is one of the identifier that you previously grab after the
insertion of the records.

8. Try to open now with embedded mode using
`http://localhost:5000/RECORD_ID/preview`

9. Open now the record that contains several files (The last record created).
By default, it is showing the first document, but you can set another file
using a query string like
`http://localhost:5000/RECORD_ID/preview?filename=square.csv`

"""

from __future__ import absolute_import, print_function

import os

from flask import Flask
from flask_babelex import Babel
from flask_cli import FlaskCLI
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB
from invenio_records import InvenioRecords

from invenio_previewer import InvenioPreviewer

# Create Flask application
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
)
Babel(app)
FlaskCLI(app)
InvenioDB(app)
InvenioRecords(app)
InvenioPreviewer(app)
InvenioAssets(app)
