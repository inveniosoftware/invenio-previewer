# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2025 CERN.
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

import importlib
from importlib.metadata import EntryPoint

import pytest
from flask import Flask
from mock import patch

from invenio_previewer import InvenioPreviewer


class MockEntryPoint(EntryPoint):
    """Mocking of entrypoint."""

    def load(self):
        """Mock load entry point."""
        return importlib.import_module(self.module)


def _mock_entry_points(group=None):
    """Mocking funtion of entrypoints."""
    data = {
        "invenio_previewer.previewers": [
            MockEntryPoint(
                name="default",
                value="invenio_previewer.extensions.default",
                group="invenio_previewer.previewers",
            ),
            MockEntryPoint(
                name="zip",
                value="invenio_previewer.extensions.zip",
                group="invenio_previewer.previewers",
            ),
        ],
    }
    names = data.keys() if group is None else [group]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


def test_version():
    """Test version import."""
    from invenio_previewer import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    InvenioPreviewer(app)
    assert "invenio-previewer" in app.extensions


@patch("importlib.metadata.entry_points", _mock_entry_points)
def test_entrypoint_previewer():
    """Test the entry points."""
    app = Flask("testapp")
    ext = InvenioPreviewer(app)
    ext.load_entry_point_group("invenio_previewer.previewers")
    assert len(ext.previewers) == 2


def test_register_previewer_duplicate():
    """Test previewer duplicate registration handling."""
    app = Flask("testapp")
    ext = InvenioPreviewer(app)

    # Mock previewer modules
    class MockPreviewer1:
        previewable_extensions = [".txt"]

    class MockPreviewer2:
        previewable_extensions = [".pdf"]

    previewer1 = MockPreviewer1()
    previewer2 = MockPreviewer2()

    # Test normal registration
    ext.register_previewer("test", previewer1)
    assert ext.previewers["test"] is previewer1

    # Test same instance re-registration (should be silent)
    ext.register_previewer("test", previewer1)
    assert ext.previewers["test"] is previewer1

    # Test different instance registration (should raise RuntimeError)
    with pytest.raises(
        RuntimeError,
        match="already registered with instance.*cannot register different instance",
    ):
        ext.register_previewer("test", previewer2)

    # Ensure original previewer is still registered
    assert ext.previewers["test"] is previewer1
