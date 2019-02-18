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

r"""Invenio module for previewing files.

Invenio-Previewer provides extensible file previewers for Invenio. It
integrates with Invenio-Records-UI via a custom view function. Currently the
module comes with viewers for the following files types:

- PDF (using PDF.js)
- ZIP
- CSV (using d3.js)
- Markdown (using Mistune library)
- XML and JSON (using Prism.js)
- Simple images (PNG, JPG, GIF)

Invenio-Previewer only provides the front-end layer for displaying previews
of files. Specifically Invenio-Previewer does not take care of generating
derived formats such thumbnails etc.
"""

from __future__ import absolute_import, print_function

from .ext import InvenioPreviewer
from .proxies import current_previewer
from .version import __version__

__all__ = ('__version__', 'current_previewer', 'InvenioPreviewer')
