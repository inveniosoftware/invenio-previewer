# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
import uuid
from zipfile import ZipFile

import pytest
from flask import Flask
from flask_webpackext import current_webpack
from invenio_assets import InvenioAssets
from invenio_config import InvenioConfigDefault
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Location, ObjectVersion
from invenio_formatter import InvenioFormatter
from invenio_i18n import Babel
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records import InvenioRecords
from invenio_records_files.api import Record
from invenio_records_ui import InvenioRecordsUI
from invenio_records_ui.views import create_blueprint_from_app
from six import BytesIO
from sqlalchemy_utils.functions import create_database, database_exists

from invenio_previewer import InvenioPreviewer


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    """Flask application fixture with database initialization."""
    instance_path = tempfile.mkdtemp()

    app_ = Flask(
        'testapp', static_folder=instance_path, instance_path=instance_path)
    app_.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///:memory:'),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
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
                record_class='invenio_records_files.api:Record',
            ),
            recid_files=dict(
                pid_type='recid',
                route='/record/<pid_value>/files/<filename>',
                view_imp='invenio_records_files.utils.file_download_ui',
                record_class='invenio_records_files.api:Record',
            ),
        ),
        SERVER_NAME='localhost',
        APP_THEME=['semantic-ui']
    )
    Babel(app_)
    InvenioAssets(app_)
    InvenioDB(app_)
    InvenioRecords(app_)
    InvenioConfigDefault(app_)
    InvenioFormatter(app_)
    InvenioPreviewer(app_)._state
    InvenioRecordsUI(app_)
    app_.register_blueprint(create_blueprint_from_app(app_))
    InvenioFilesREST(app_)

    with app_.app_context():
        yield app_

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Setup database."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()
    yield db_
    db_.session.remove()
    db_.drop_all()


@pytest.yield_fixture(scope='session')
def webassets(app):
    """Flask application fixture with assets."""
    initial_dir = os.getcwd()
    os.chdir(app.instance_path)
    # force theme.config alias pinting to less/invenio_theme/theme.config
    theme_bundle = current_webpack.project.bundles[0]
    theme_bundle.aliases['../../theme.config'] = \
        'less/invenio_theme/theme.config'
    current_webpack.project.buildall()
    yield app
    os.chdir(initial_dir)


@pytest.yield_fixture()
def location(db):
    """File system location."""
    tmppath = tempfile.mkdtemp()

    loc = Location(
        name='testloc',
        uri=tmppath,
        default=True
    )
    db.session.add(loc)
    db.session.commit()

    yield loc

    shutil.rmtree(tmppath)


@pytest.fixture()
def record(db, location):
    """Record fixture."""
    rec_uuid = uuid.uuid4()
    provider = RecordIdProvider.create(
        object_type='rec', object_uuid=rec_uuid)
    record = Record.create({
        'control_number': provider.pid.pid_value,
        'title': 'TestDefault',
    }, id_=rec_uuid)
    db.session.commit()
    return record


@pytest.fixture()
def record_with_file(db, record, location):
    """Record with a test file."""
    testfile = ObjectVersion.create(record.bucket, 'testfile',
                                    stream=BytesIO(b'atest'))
    record.update(dict(
        _files=[dict(
            bucket=str(testfile.bucket_id),
            key=testfile.key,
            size=testfile.file.size,
            checksum=str(testfile.file.checksum),
            version_id=str(testfile.version_id),
        ), ]
    ))
    record.commit()
    db.session.commit()
    return record, testfile


@pytest.fixture()
def zip_fp(db):
    """ZIP file stream."""
    fp = BytesIO()

    zipf = ZipFile(fp, 'w')
    zipf.writestr('Example.txt', 'This is an example'.encode('utf-8'))
    zipf.writestr(u'Lé UTF8 test.txt', 'This is an example'.encode('utf-8'))
    zipf.close()

    fp.seek(0)
    return fp
