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
