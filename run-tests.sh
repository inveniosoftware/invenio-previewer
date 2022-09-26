#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

python -m check_manifest --ignore ".*-requirements.txt" && \
python -m setup extract_messages --dry-run
python -m sphinx.cmd.build -qnNW docs docs/_build/html && \
python -m pytest
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
tests_exit_code=$?
exit "$tests_exit_code"
