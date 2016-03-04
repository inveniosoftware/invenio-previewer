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


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import subprocess
import tempfile

import pytest
from click.testing import CliRunner
from flask import Flask
from flask_babelex import Babel
from flask_cli import FlaskCLI, ScriptInfo
from invenio_assets import InvenioAssets
from invenio_assets.cli import assets, collect, npm
from invenio_db import InvenioDB, db
from invenio_records import InvenioRecords
from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from invenio_previewer import InvenioPreviewer
from invenio_previewer.extensions import csv_dthreejs, default, mistune, \
    pdfjs, zip
from invenio_records_ui import InvenioRecordsUI


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True
    )
    InvenioPreviewer(app)
    return app


@pytest.fixture()
def app_db(request):
    """Flask application fixture with database initialization."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    )
    FlaskCLI(app)
    InvenioDB(app)
    InvenioRecords(app)
    InvenioPreviewer(app)

    with app.app_context():
        if not database_exists(str(db.engine.url)):
            create_database(str(db.engine.url))
        db.create_all()

    def teardown():
        with app.app_context():
            drop_database(str(db.engine.url))
    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def app_assets(request):
    """Flask application fixture with assets."""
    initial_dir = os.getcwd()
    instance_path = tempfile.mkdtemp()
    os.chdir(instance_path)
    app = Flask('testapp',
                static_folder=instance_path,
                instance_path=instance_path)
    app.config.update(dict(
        RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
        RECORDS_UI_ENDPOINTS=dict(
            recid=dict(
                pid_type='recid',
                route='/records/<pid_value>',
                template='invenio_records_ui/detail.html',
            ),
            recid_previewer=dict(
                pid_type='recid',
                route='/records/<pid_value>/preview',
                view_imp='invenio_previewer.views:preview',
            ),
        )
    ))
    Babel(app)
    FlaskCLI(app)
    InvenioAssets(app)
    previewer = InvenioPreviewer(app)
    InvenioRecordsUI(app)
    previewer.register_previewer(zip)
    previewer.register_previewer(mistune)
    previewer.register_previewer(pdfjs)
    previewer.register_previewer(csv_dthreejs)
    previewer.register_previewer(default)

    script_info = ScriptInfo(create_app=lambda info: app)
    script_info._loaded_app = app

    runner = CliRunner()
    runner.invoke(npm, obj=script_info)

    subprocess.call(["npm", "install", instance_path])
    runner.invoke(collect, ['-v'], obj=script_info)
    runner.invoke(assets, ['build'], obj=script_info)

    def teardown():
        shutil.rmtree(instance_path)
        os.chdir(initial_dir)
    request.addfinalizer(teardown)
    return app
