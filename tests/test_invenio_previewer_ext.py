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


"""Module tests."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
import zipfile

from invenio_previewer.previewerext import csv_dthreejs, default, mistune, \
    pdfjs, zip
from invenio_previewer.views import DocumentPreviewer


class FakeDocument(object):
    """Fake class emulating the behaviour required in a Invenio-Document"""

    def __init__(self, uri):
        """Document initialization."""
        self.uri = uri


def test_mistune_can_preview():
    """Test can_preview method in mistune extension."""
    fake_document = FakeDocument('/example/markdown.md')
    document_previewer = DocumentPreviewer(0, fake_document)
    assert mistune.can_preview(document_previewer)


def test_mistune_preview(app_assets):
    """Test preview method in mistune extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'markdown.md'))
        with open(fake_document.uri, 'w') as file:
            file.write("### Testing markdown ###")
        document_previewer = DocumentPreviewer(0, fake_document)
        assert '<h3>Testing markdown</h3>\n' in mistune.preview(
            document_previewer)
        shutil.rmtree(tmpdirname)


def test_default_can_preview():
    """Test can_preview method in default extension."""
    assert default.can_preview(None) is True


def test_default_preview(app_assets):
    """Test preview method in default extension."""
    with app_assets.test_request_context():
        assert 'we are unfortunately not able' in default.preview(None)


def test_csv_dthreejs_invalid_delimiter(app_assets):
    """Test can_preview method in csv recline extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'comma.csv'))
        with open(fake_document.uri, 'w') as file:
            file.write("A&'B'^C\n1,5%7")
        document_previewer = DocumentPreviewer(0, fake_document)
        assert not csv_dthreejs.can_preview(document_previewer)
        shutil.rmtree(tmpdirname)


def test_csv_dthreejs_can_preview(app_assets):
    """Test can_preview method in csv recline extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'comma.csv'))
        with open(fake_document.uri, 'w') as file:
            file.write("A,B\n1,2")
        document_previewer = DocumentPreviewer(0, fake_document)
        assert csv_dthreejs.can_preview(document_previewer)
        shutil.rmtree(tmpdirname)


def test_csv_dthreejs_preview(app_assets):
    """Test preview method in dthtreejs extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'comma.csv'))
        with open(fake_document.uri, 'w') as file:
            file.write("A,B\n1,2")
        document_previewer = DocumentPreviewer(0, fake_document)
        assert 'data-csv-source="/document/0/comma.csv"' \
               in csv_dthreejs.preview(document_previewer)
        shutil.rmtree(tmpdirname)


def test_pdfjs_can_preview():
    """Test can_preview method in csv recline extension."""
    document = FakeDocument('PDFFile.pdf')
    document_previewer = DocumentPreviewer('0', document)
    assert pdfjs.can_preview(document_previewer)


def test_pdfjs_preview(app_assets):
    """Test preview method in pdfjs extension."""
    with app_assets.test_request_context():
        document = FakeDocument('PDFFile.pdf')
        document_previewer = DocumentPreviewer('0', document)
        assert 'DFFile.pdf\');'\
               in pdfjs.preview(document_previewer)


def test_zip_can_preview():
    """Test can_preview method in csv recline extension."""
    document = FakeDocument('ZipFile.zip')
    document_previewer = DocumentPreviewer('0', document)
    assert zip.can_preview(document_previewer)


def test_zip_preview(app_assets):
    """Test preview method in zip extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'zip.zip'))
        zipf = zipfile.ZipFile(fake_document.uri, 'w')
        zipf.writestr('Example.txt', 'This is an example')
        zipf.close()
        document_previewer = DocumentPreviewer(0, fake_document)
        assert 'Example.txt' in zip.preview(document_previewer)
        shutil.rmtree(tmpdirname)


def test_zip_children(app_assets):
    """Test preview method in zip extension."""
    with app_assets.test_request_context():
        tmpdirname = tempfile.mktemp()
        if not os.path.exists(tmpdirname):
            os.makedirs(tmpdirname)
        fake_document = FakeDocument(
            os.path.join(tmpdirname, 'zip.zip'))
        zipf = zipfile.ZipFile(fake_document.uri, 'w')
        zipf.writestr('/a/b/c/Example.txt', 'This is a test')
        zipf.close()
        document_previewer = DocumentPreviewer(0, fake_document)
        assert 'Example.txt' in zip.preview(document_previewer)
        shutil.rmtree(tmpdirname)
