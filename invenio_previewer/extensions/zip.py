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

"""Simple ZIP archive previewer."""

from __future__ import absolute_import, print_function

import os
import zipfile

from flask import current_app, render_template

from ..proxies import current_previewer

previewable_extensions = ['zip']


def make_tree(file):
    """Create tree structure from ZIP archive."""
    max_files_count = current_app.config.get('PREVIEWER_ZIP_MAX_FILES', 1000)
    fp = file.open()
    zf = zipfile.ZipFile(fp)
    tree = {'type': 'folder', 'id': -1, 'children': {}}
    try:
        for i, info in enumerate(zf.infolist()):
            if i > max_files_count:
                raise BufferError('Too much files inside the ZIP file')
            comps = info.filename.split(os.sep)
            node = tree
            for c in comps:
                if c not in node['children']:
                    if c == '':
                        node['type'] = 'folder'
                        continue
                    node['children'][c] = {
                        'name': c, 'type': 'item', 'id': 'item{0}'.format(i),
                        'children': {}}
                node = node['children'][c]
            node['size'] = info.file_size
    except BufferError:
        return tree, True
    finally:
        fp.close()

    return tree, False


def children_to_list(node):
    """Organize children structure."""
    if node['type'] == 'item' and len(node['children']) == 0:
        del node['children']
    else:
        node['type'] = 'folder'
        node['children'] = list(node['children'].values())
        node['children'].sort(key=lambda x: x['name'])
        node['children'] = map(children_to_list, node['children'])
    return node


def can_preview(file):
    """Return True if filetype can be previewed."""
    return file.is_local() and file.has_extensions('.zip')


def preview(file):
    """Return appropriate template and pass the file and an embed flag."""
    tree, limit_reached = make_tree(file)
    list = children_to_list(tree)['children']
    return render_template(
        "invenio_previewer/zip.html",
        file=file,
        tree=list,
        limit_reached=limit_reached,
        js_bundles=current_previewer.js_bundles + ['previewer_fullscreen_js'],
        css_bundles=current_previewer.css_bundles,
    )
