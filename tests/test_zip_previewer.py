# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""ZIP previewer tests."""

import struct
import zipfile
from io import BytesIO
from unittest.mock import patch
from zlib import crc32

import pytest

from invenio_previewer.extensions import zip as zip_previewer

TOO_LARGE = "ZIP file is too large to be previewed."
TOO_MANY_FILES = "Too many files inside the ZIP file."


class CountingBytesIO(BytesIO):
    """In-memory file counting the bytes read from it."""

    bytes_read = 0

    def read(self, size=-1):
        """Read and count bytes."""
        data = super().read(size)
        self.bytes_read += len(data)
        return data


class ZipFileObject:
    """Previewer file object for an in-memory ZIP archive."""

    def __init__(self, data):
        """Constructor."""
        self.data = data
        self.size = len(data)
        self.fp = None

    def open(self):
        """Open the archive."""
        self.fp = CountingBytesIO(self.data)
        return self.fp


def make_zip(entries, comment=b"", zip64=False):
    """Create a ZIP archive, entries are names or ``(ZipInfo, data)`` tuples."""
    fp = BytesIO()
    # zipfile only writes the ZIP64 end records for more than 65535 files.
    limit = 0 if zip64 else zipfile.ZIP_FILECOUNT_LIMIT
    with patch("zipfile.ZIP_FILECOUNT_LIMIT", limit):
        with zipfile.ZipFile(fp, "w") as zf:
            for entry in entries:
                if isinstance(entry, tuple):
                    zf.writestr(*entry)
                else:
                    zf.writestr(entry, b"" if entry.endswith("/") else b"content")
            zf.comment = comment
    return fp.getvalue()


def many_files(count):
    """File names spread over a few folders."""
    return [f"folder{i % 7}/sub{i % 3}/file{i:06d}.txt" for i in range(count)]


def unicode_path_extra_entry():
    """Entry with an Info-ZIP Unicode Path extra field, as written by ``zip``."""
    info = zipfile.ZipInfo("fallback.txt")
    name = "données/été.txt".encode("utf-8")
    info.extra = (
        struct.pack("<HHB", 0x7075, 5 + len(name), 1)
        + struct.pack("<L", crc32(b"fallback.txt"))
        + name
    )
    return info, b"content"


def zip_with_large_file_size():
    """Archive declaring a file larger than 4 GiB (ZIP64 extra field)."""
    fp = BytesIO()
    with zipfile.ZipFile(fp, "w") as zf:
        zf.writestr("big.bin", b"x")
        zf.filelist[0].file_size = 5 * 2**30
    return fp.getvalue()


def make_tree_without_check(file):
    """Make the tree without checking the number of files (previous behaviour)."""
    with patch.object(
        zip_previewer, "_check_file_count", lambda fp, max_files_count: None
    ):
        return zip_previewer.make_tree(file)


ARCHIVES = {
    "empty": lambda: make_zip([]),
    "folders": lambda: make_zip(
        ["README.md", "data/", "data/a.csv", "data/sub/b.csv", "a/b/c/d.txt", "e/"]
    ),
    "utf8-names": lambda: make_zip(["Lé UTF8 test.txt", "日本語/ファイル.txt"]),
    # zipfile always writes ASCII or UTF-8, rewrite the raw name bytes instead.
    "cp437-names": lambda: make_zip(["cafe.txt"]).replace(b"cafe.txt", b"caf\x82.txt"),
    "unicode-path-extra": lambda: make_zip([unicode_path_extra_entry()]),
    "large-file-size": zip_with_large_file_size,
    "comment": lambda: make_zip(["a.txt", "b/c.txt"], comment=b"PK" * 1000),
    "prepended-data": lambda: b"#!/bin/sh\n" * 100 + make_zip(["a.txt", "b/c.txt"]),
    "zip64": lambda: make_zip(many_files(20), zip64=True),
    "zip64-prepended-data": lambda: b"\x00" * 1000
    + make_zip(many_files(20), zip64=True),
    "max-files": lambda: make_zip(many_files(1000)),
}


@pytest.mark.parametrize("name", ARCHIVES)
def test_zip_preview(testapp, name):
    """Test archives within the limits are previewed as without the checks."""
    data = ARCHIVES[name]()
    with testapp.app_context():
        result = zip_previewer.make_tree(ZipFileObject(data))
        assert result == make_tree_without_check(ZipFileObject(data))

    tree, limit_reached, error = result
    assert (limit_reached, error) == (False, None)


@pytest.mark.parametrize("zip64", [False, True])
@pytest.mark.parametrize("count", [0, 1, 5, 6, 100])
def test_zip_preview_max_files(testapp, count, zip64):
    """Test archives with more files than PREVIEWER_ZIP_MAX_FILES are not previewed."""
    data = make_zip(many_files(count), zip64=zip64)
    with patch.dict(testapp.config, {"PREVIEWER_ZIP_MAX_FILES": 5}):
        with testapp.app_context():
            tree, limit_reached, error = zip_previewer.make_tree(ZipFileObject(data))

    assert error == (TOO_MANY_FILES if count > 5 else None)
    assert limit_reached is False


@pytest.mark.parametrize(
    "size, expected_error", [(100 * 2**20, None), (100 * 2**20 + 1, TOO_LARGE)]
)
def test_zip_preview_max_bytes(testapp, size, expected_error):
    """Test archives larger than PREVIEWER_ZIP_MAX_BYTES are not previewed."""
    file = ZipFileObject(make_zip(["a.txt", "b/c.txt"]))
    # Only the size of the file is checked, the archive itself can stay small.
    file.size = size
    with testapp.app_context():
        tree, limit_reached, error = zip_previewer.make_tree(file)

    assert error == expected_error
    if expected_error:
        assert file.fp is None


def test_zip_preview_reads_only_the_end_of_large_archives(testapp):
    """Test archives with many files are not previewed, reading only the end."""
    data = make_zip(many_files(100000))
    file = ZipFileObject(data)
    with testapp.app_context():
        tree, limit_reached, error = zip_previewer.make_tree(file)

    assert error == TOO_MANY_FILES
    assert len(data) > 10 * 2**20
    assert file.fp.bytes_read < 128 * 2**10


def test_zip_preview_not_a_zip(testapp):
    """Test files which are not ZIP archives are not previewed."""
    file = ZipFileObject(b"This is not a ZIP file" * 10)
    with testapp.app_context():
        tree, limit_reached, error = zip_previewer.make_tree(file)

    assert error == "File is not a ZIP file"
