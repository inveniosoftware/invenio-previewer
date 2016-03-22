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

from flask import render_template_string, url_for
from invenio_db import db
from invenio_files_rest.models import ObjectVersion
from six import BytesIO


def create_file(record, bucket, filename, stream):
    """Create a file and add in record."""
    ObjectVersion.create(bucket, filename, stream=stream)
    record.update(dict(
        files=[dict(
            uri='/files/{0}/{1}'.format(str(bucket.id), filename),
            bucket=str(bucket.id),
            filename=filename,
        ), ]
    ))
    record.commit()
    db.session.commit()


def preview_url(pid_val, filename):
    """Preview URL."""
    return url_for('invenio_records_ui.recid_previewer',
                   pid_value=pid_val, filename=filename)


def test_default_extension(app, db, webassets, bucket, record):
    """Test view by default."""
    create_file(record, bucket, 'testfile', BytesIO(b'empty'))

    with app.test_client() as client:
        res = client.get(preview_url(record['recid'], 'testfile'))
        assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_markdown_extension(app, db, webassets, bucket, record):
    """Test view with md files."""
    create_file(
        record, bucket, 'markdown.md', BytesIO(b'### Testing markdown ###'))

    with app.test_client() as client:
        res = client.get(preview_url(record['recid'], 'markdown.md'))
        assert '<h3>Testing markdown' in res.get_data(as_text=True)


def test_pdf_extension(app, db, webassets, bucket, record):
    """Test view with pdf files."""
    create_file(
        record, bucket, 'test.pdf', BytesIO(b'Content not used'))

    with app.test_client() as client:
        res = client.get(preview_url(record['recid'], 'test.pdf'))
        assert 'PDFView.open(\'' in res.get_data(as_text=True)


def test_csv_dthreejs_extension(app, db, webassets, bucket, record):
    """Test view with pdf files."""
    create_file(
        record, bucket, 'test.csv', BytesIO(b'A,B\n1,2'))

    with app.test_client() as client:
        res = client.get(preview_url(record['recid'], 'test.csv'))
        assert 'data-csv-source="' in res.get_data(as_text=True)


def test_zip_extension(app, db, webassets, bucket, record, zip_fp):
    """Test view with pdf files."""
    create_file(
        record, bucket, 'test.zip', zip_fp)

    with app.test_client() as client:
        res = client.get(preview_url(record['recid'], 'test.zip'))
        assert 'Example.txt' in res.get_data(as_text=True)


def test_view_macro_file_list(app):
    """Test file list macro."""
    with app.test_request_context():
        files = [
            {
                'uri': 'http://domain/test1.txt',
                'filename': 'test1.txt',
                'size': 10,
                'date': '2016-07-12',
            },
            {
                'uri': 'http://otherdomain/test2.txt',
                'filename': 'test2.txt',
                'size': 12,
                'date': '2016-07-12',
            },
        ]

        result = render_template_string("""
            {%- from "invenio_previewer/macros.html" import file_list %}
            {{ file_list(files) }}
            """, files=files)

        assert '<a class="forcewrap" href="http://domain/test1.txt"' in result
        assert '<td class="nowrap">2016-07-12' in result
        assert '<td class="nowrap">10</td>' in result
        assert 'href="http://otherdomain/test2.txt"' in result
        assert '<td class="nowrap">2016-07-12</td>' in result
        assert '<td class="nowrap">12</td>' in result
