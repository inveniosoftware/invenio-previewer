..
    SPDX-FileCopyrightText: 2016-2019 CERN.
    SPDX-License-Identifier: MIT

Installation
============

Invenio-Previewer is on PyPI so all you need is::

    pip install invenio-previewer

Invenio-Previewer depends on Invenio-Assets for assets bundling and Invenio-PidStore and Invenio-Records-UI for record
integration.

You will normally use it in combination with files. You can install the extra Invenio modules Invenio-Files-REST
and Invenio-Records-Files by specifying the ``files`` key in extras::

    pip install invenio-previewer[files]
