# SPDX-FileCopyrightText: 2015-2019 CERN.
# SPDX-FileCopyrightText: 2023 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Simple ZIP archive previewer."""

import os
import zipfile

from charset_normalizer import detect
from flask import current_app, render_template
from invenio_i18n import gettext as _

from ..proxies import current_previewer

previewable_extensions = ["zip"]


def _open_zip(fp, max_files_count):
    """Open a ZIP archive, raising LargeZipFile if it has too many files.

    ``zipfile`` loads the whole central directory (table of contents) in memory
    when opening an archive. The number of files and the size of the central
    directory are therefore checked first, reading only the end of the archive.
    The declared number of files can be understated, so the files are also
    counted after parsing.
    """
    # A similar check exists in invenio-records-resources: keep them aligned.
    endrec = zipfile._EndRecData(fp)
    if not endrec:
        raise zipfile.BadZipFile(_("File is not a ZIP file"))
    if endrec[zipfile._ECD_ENTRIES_TOTAL] > max_files_count:
        raise zipfile.LargeZipFile(_("Too many files inside the ZIP file."))
    # The declared number of files can be fake, so also limit the size of the
    # table of contents. 512 bytes per file is generous: it is mostly the file name.
    if endrec[zipfile._ECD_SIZE] > max_files_count * 512:
        raise zipfile.LargeZipFile(_("ZIP file is too large to be previewed."))
    zf = zipfile.ZipFile(fp)
    if len(zf.infolist()) > max_files_count:
        raise zipfile.LargeZipFile(_("Too many files inside the ZIP file."))
    return zf


def make_tree(file):
    """Create tree structure from ZIP archive."""
    max_files_count = current_app.config["PREVIEWER_ZIP_MAX_FILES"]
    max_file_size = current_app.config["PREVIEWER_ZIP_MAX_BYTES"]
    tree = {"type": "folder", "id": -1, "children": {}}

    try:
        if file.size > max_file_size:
            raise zipfile.LargeZipFile(_("ZIP file is too large to be previewed."))
        with file.open() as fp:
            zf = _open_zip(fp, max_files_count)
            # Detect filenames encoding.
            sample = " ".join(zf.namelist()[:max_files_count])
            if not isinstance(sample, bytes):
                sample = sample.encode("utf-16be")
            encoding = detect(sample).get("encoding", "utf-8")
            for i, info in enumerate(zf.infolist()):
                comps = info.filename.split(os.sep)
                node = tree
                for c in comps:
                    if not isinstance(c, str):
                        c = c.decode(encoding)
                    if c not in node["children"]:
                        if c == "":
                            node["type"] = "folder"
                            continue
                        node["children"][c] = {
                            "name": c,
                            "type": "item",
                            "id": "item{0}".format(i),
                            "children": {},
                        }
                    node = node["children"][c]
                node["size"] = info.file_size
    except (zipfile.BadZipFile, zipfile.LargeZipFile) as e:
        return tree, False, str(e)
    except Exception as e:
        current_app.logger.warning(str(e), exc_info=True)
        return tree, False, _("ZIP file is not previewable.")

    return tree, False, None


def children_to_list(node):
    """Organize children structure."""
    if node["type"] == "item" and len(node["children"]) == 0:
        del node["children"]
    else:
        node["type"] = "folder"
        node["children"] = list(node["children"].values())
        node["children"].sort(key=lambda x: x["name"])
        node["children"] = map(children_to_list, node["children"])
    return node


def can_preview(file):
    """Return True if filetype can be previewed."""
    return file.is_local() and file.has_extensions(".zip")


def preview(file):
    """Return the appropriate template and pass the file and an embed flag."""
    tree, limit_reached, error = make_tree(file)
    list = children_to_list(tree)["children"]
    return render_template(
        "invenio_previewer/zip.html",
        file=file,
        tree=list,
        limit_reached=limit_reached,
        error=error,
        js_bundles=current_previewer.js_bundles,
        css_bundles=current_previewer.css_bundles + ["zip_css.css"],
    )
