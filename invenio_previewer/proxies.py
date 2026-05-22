# SPDX-FileCopyrightText: 2016-2019 CERN.
# SPDX-License-Identifier: MIT

"""Proxy for current previewer."""

from flask import current_app
from werkzeug.local import LocalProxy

current_previewer = LocalProxy(lambda: current_app.extensions["invenio-previewer"])
"""Proxy object to the current previewer extension."""
