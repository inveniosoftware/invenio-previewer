# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Previewer Utilities."""

import cchardet
from flask import current_app


def detect_encoding(fp, default=None):
    """Detect the character encoding of a file.

    :param fp: Open Python file pointer.
    :param default: Fallback encoding to use.
    :returns: The detected encoding.

    .. note:: The file pointer is returned at its original read position.
    """
    init_pos = fp.tell()
    try:
        sample = fp.read(
            current_app.config.get('PREVIEWER_CHARDET_BYTES', 1024))
        # Result contains 'confidence' and 'encoding'
        result = cchardet.detect(sample)
        threshold = current_app.config.get('PREVIEWER_CHARDET_CONFIDENCE', 0.9)
        if result.get('confidence', 0) > threshold:
            return result.get('encoding', default)
        else:
            return default
    except Exception:
        current_app.logger.warning('Encoding detection failed.', exc_info=True)
        return default
    finally:
        fp.seek(init_pos)
