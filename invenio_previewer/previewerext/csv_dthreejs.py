# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2013, 2014, 2015, 2016 CERN.
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

"""Render Bar chart from csv file."""

import csv
import os

from chardet.universaldetector import UniversalDetector

from flask import current_app, render_template


def validate_csv(document):
    """Return dialect information about given csv file."""
    with open(document.document.uri, 'rU') as csvfile:
        is_valid = False
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
        except Exception as e:
            current_app.logger.debug(
                'File %s is not valid CSV: %s' % (document.get_filename(), e))
            return {
                'delimiter': '',
                'encoding': '',
                'is_valid': is_valid
            }
        universal_detector = UniversalDetector()
        dialect.strict = True
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        try:
            for row in reader:
                universal_detector.feed(
                    dialect.delimiter.join(row).encode('utf-8'))
            is_valid = True
        except csv.Error as e:
            current_app.logger.debug(
                'File %s is not valid CSV: %s' % (document.get_filename(), e))
        finally:
            universal_detector.close()
    return {
        'delimiter': dialect.delimiter,
        'encoding': universal_detector.result['encoding'],
        'is_valid': is_valid
    }


def can_preview(document):
    """Determine if the given file can be previewed."""
    if document.extension == 'csv':
        return validate_csv(document)['is_valid']
    else:
        return False


def preview(document):
    """Render appropiate template with embed flag."""
    file_info = validate_csv(document)
    return render_template("invenio_previewer/csv_bar.html", f=document,
                           delimiter=file_info['delimiter'],
                           encoding=file_info['encoding'])
