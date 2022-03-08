# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

pydocstyle invenio_previewer
python -m check_manifest --ignore ".*-requirements.txt"
sphinx-build -qnNW docs docs/_build/html
python -m pytest
tests_exit_code=$?
sphinx-build -qnNW -b doctest docs docs/_build/doctest
exit "$tests_exit_code"
