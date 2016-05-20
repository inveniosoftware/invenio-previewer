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

"""Markdown rendering using mistune library."""

from __future__ import absolute_import, unicode_literals

from flask import render_template

import mistune


previewable_extensions = ['md']


def render(file):
    """Render HTML from Markdown file content."""
    fp = file.open()
    content = fp.read()
    result = mistune.markdown(content.decode('utf-8'))
    fp.close()
    return result


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions('.md')


def preview(file):
    """Render Markdown."""
    return render_template("invenio_previewer/mistune.html",
                           file=file,
                           content=render(file))
