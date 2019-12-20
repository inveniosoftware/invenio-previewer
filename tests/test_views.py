# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views module tests."""

from __future__ import absolute_import, print_function

from flask import render_template_string


def test_view_macro_file_list(app):
    """Test file list macro."""
    with app.test_request_context():
        files = [
            {
                'key': 'test1.txt',
                'size': 10,
                'date': '2016-07-12',
            },
            {
                'key': 'test2.txt',
                'size': 12000000,
                'date': '2016-07-12',
            },
        ]

        pid = {
            'pid_value': 1
        }

        result = render_template_string("""
            {%- from "invenio_previewer/macros.html" import file_list %}
            {{ file_list(files, pid) }}
            """, files=files, pid=pid)

        assert 'href="/record/1/files/test1.txt?download=1"' in result
        assert '<td class="nowrap">10 Bytes</td>' in result
        assert 'href="/record/1/files/test2.txt?download=1"' in result
        assert '<td class="nowrap">12.0 MB</td>' in result


def test_previwable_test(app):
    """Test template test."""
    file = {
        'type': 'md'
    }
    template = "{% if file.type is previewable %}Previwable" \
               "{% else %}Not previwable{% endif %}"
    assert render_template_string(template, file=file) == "Previwable"

    file['type'] = 'no'
    assert render_template_string(template, file=file) == "Not previwable"

    file['type'] = 'pdf'
    assert render_template_string(template, file=file) == "Previwable"

    file['type'] = ''
    assert render_template_string(template, file=file) == "Not previwable"
