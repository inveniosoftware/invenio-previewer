# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views module tests."""

from __future__ import absolute_import, print_function

import zipfile

from flask import render_template_string, url_for
from invenio_db import db
from invenio_files_rest.models import ObjectVersion
from mock import patch
from six import BytesIO, b


def create_file(record, filename, stream):
    """Create a file and add in record."""
    obj = ObjectVersion.create(record.bucket, filename, stream=stream)
    record.update(dict(
        _files=[dict(
            bucket=str(record.bucket.id),
            key=filename,
            size=obj.file.size,
            checksum=str(obj.file.checksum),
            version_id=str(obj.version_id),
        ), ]
    ))
    record.commit()
    db.session.commit()


def preview_url(pid_val, filename):
    """Preview URL."""
    return url_for('invenio_records_ui.recid_previewer',
                   pid_value=pid_val, filename=filename)


def test_default_extension(app, webassets, record):
    """Test view by default."""
    create_file(record, 'testfile', BytesIO(b'empty'))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'testfile'))
        assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_markdown_extension(app, webassets, record):
    """Test view with md files."""
    create_file(
        record, 'markdown.md', BytesIO(b'### Testing markdown ###'))
    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'markdown.md'))
        assert '<h3>Testing markdown' in res.get_data(as_text=True)
        with patch('mistune.markdown', side_effect=Exception):
            res = client.get(preview_url(record['control_number'],
                                         'markdown.md'))
            assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_pdf_extension(app, webassets, record):
    """Test view with pdf files."""
    create_file(
        record, 'test.pdf', BytesIO(b'Content not used'))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.pdf'))
        assert 'PDFView.open(\'' in res.get_data(as_text=True)


def test_csv_dthreejs_extension(app, webassets, record):
    """Test view with csv files."""
    create_file(record, 'test.csv', BytesIO(b'A,B\n1,2'))
    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.csv'))
        assert 'data-csv-source="' in res.get_data(as_text=True)
        assert 'data-csv-delimiter=","' in res.get_data(as_text=True)

        with patch('csv.Sniffer', side_effect=Exception):
            res = client.get(preview_url(record['control_number'], 'test.csv'))
            assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_csv_dthreejs_delimiter(app, webassets, record):
    """Test view with csv files."""
    create_file(record, 'test.csv', BytesIO(b'A#B\n1#2'))
    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.csv'))
        assert 'data-csv-source="' in res.get_data(as_text=True)
        assert 'data-csv-delimiter="#"' in res.get_data(as_text=True)


def test_zip_extension(app, webassets, record, zip_fp):
    """Test view with a zip file."""
    create_file(
        record, 'test.zip', zip_fp)

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.zip'))
        assert 'Example.txt' in res.get_data(as_text=True)
        assert u'Lé UTF8 test.txt' in res.get_data(as_text=True)

        with patch('zipfile.ZipFile', side_effect=zipfile.LargeZipFile):
            res = client.get(preview_url(record['control_number'], 'test.zip'))
            assert 'Zipfile is too large' in res.get_data(as_text=True)

        with patch('zipfile.ZipFile', side_effect=Exception):
            res = client.get(preview_url(record['control_number'], 'test.zip'))
            assert 'Zipfile is not previewable' in res.get_data(as_text=True)


def test_json_extension(app, webassets, record):
    """Test view with JSON files."""
    json_data = '{"name":"invenio","num":42,'\
                '"flt":3.14159,"lst":[1,2,3],'\
                '"obj":{"field":"<script>alert(1)</script>","num":4}}'
    create_file(record, 'test.json', BytesIO(b(json_data)))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.json'))
        assert 'class="language-javascript"' in res.get_data(as_text=True)

        rendered_json = \
            '{\n' \
            '    &#34;name&#34;: &#34;invenio&#34;,\n' \
            '    &#34;num&#34;: 42,\n' \
            '    &#34;flt&#34;: 3.14159,\n' \
            '    &#34;lst&#34;: [\n' \
            '        1,\n' \
            '        2,\n' \
            '        3\n' \
            '    ],\n' \
            '    &#34;obj&#34;: {\n' \
            '        &#34;field&#34;: &#34;&lt;script&gt;alert(1)' \
            '&lt;/script&gt;&#34;,\n' \
            '        &#34;num&#34;: 4\n' \
            '    }\n' \
            '}'
        assert rendered_json in res.get_data(as_text=True)

        with patch('json.dumps', side_effect=Exception):
            res = client.get(preview_url(record['control_number'],
                                         'test.json'))
            assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_max_file_size(app, webassets, record):
    """Test file size limitation."""
    max_file_size = app.config.get(
        'PREVIEWER_MAX_FILE_SIZE_BYTES', 1 * 1024 * 1024)
    too_large_string = '1' * (max_file_size + 1)
    create_file(record, 'test.json', BytesIO(b(too_large_string)))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.json'))
        assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_xml_extension(app, webassets, record):
    """Test view with XML files."""
    xml_data = b'<el a="some"><script>alert(1)</script><c>1</c><c>2</c></el>'
    create_file(
        record, 'test.xml', BytesIO(xml_data))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.xml'))
        assert 'class="language-markup"' in res.get_data(as_text=True)
        assert '&lt;el a=&#34;some&#34;&gt;' in res.get_data(as_text=True)
        assert '&lt;c&gt;1&lt;/c&gt;' in res.get_data(as_text=True)
        assert '&lt;c&gt;2&lt;/c&gt;' in res.get_data(as_text=True)
        assert '&lt;/el&gt;' in res.get_data(as_text=True)

        with patch('xml.dom.minidom.Node.toprettyxml', side_effect=Exception):
            res = client.get(preview_url(record['control_number'], 'test.xml'))
            assert 'we are unfortunately not' in res.get_data(as_text=True)


def test_ipynb_extension(app, webassets, record):
    """Test view with IPython notebooks files."""
    create_file(
        record, 'test.ipynb', BytesIO(b'''
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "This is an example notebook."
      ]
    }
  ],
  "metadata":{
      "kernelspec":{
         "display_name":"Python 2",
         "language":"python",
         "name":"python2"
      },
      "language_info":{
         "codemirror_mode":{
            "name":"ipython",
            "version":2
         },
         "file_extension":".py",
         "mimetype":"text/x-python",
         "name":"python",
         "nbconvert_exporter":"python",
         "pygments_lexer":"ipython2",
         "version":"2.7.10"
      }
   },
  "nbformat":4,
  "nbformat_minor":0
}'''))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.ipynb'))
        assert 'This is an example notebook.' in res.get_data(as_text=True)


def test_simple_image_extension(app, webassets, record):
    """Test view with simple image files (PNG)."""
    create_file(record, 'test.png', BytesIO(b'Content not used'))

    with app.test_client() as client:
        res = client.get(preview_url(record['control_number'], 'test.png'))
        assert '<img src="' in res.get_data(as_text=True)
        assert 'style="max-width: 100%;">' in res.get_data(as_text=True)


def test_view_macro_file_list(app):
    """Test file list macro."""
    with app.test_request_context():
        files = [
            {
                'uri': 'http://domain/test1.txt',
                'key': 'test1.txt',
                'size': 10,
                'date': '2016-07-12',
            },
            {
                'uri': 'http://otherdomain/test2.txt',
                'key': 'test2.txt',
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
