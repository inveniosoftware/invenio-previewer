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

"""Test of utilities module."""

from __future__ import absolute_import, print_function

from mock import patch
from six import BytesIO

from invenio_previewer import current_previewer
from invenio_previewer.utils import detect_encoding


def test_default_file_reader(app, record_with_file, testfile):
    """Test view by default."""
    file_ = current_previewer.record_file_factory(
        None, record_with_file, testfile.key)
    assert file_.version_id == testfile.version_id


def test_detect_encoding(app):
    """Test encoding detection."""
    f = BytesIO(u'Γκρήκ Στρίνγκ'.encode('utf-8'))
    initial_position = f.tell()
    assert detect_encoding(f).lower() == 'utf-8'
    assert f.tell() == initial_position

    with patch('cchardet.detect', Exception):
        assert detect_encoding(f) is None
