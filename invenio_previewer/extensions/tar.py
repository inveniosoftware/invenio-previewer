from __future__ import absolute_import, print_function

import os
import tarfile

import cchardet as chardet
from flask import current_app, render_template
from six import binary_type

from .._compat import text_type
from ..proxies import current_previewer

previewable_extensions = ['tar', 'gz', 'bz2', 'tgz', 'tbz', 'tbz2']


def make_tree(file):
    """Create tree structure from tar archives."""
    max_files_count = current_app.config.get('PREVIEWER_ZIP_MAX_FILES', 1000)
    tree = {'type': 'folder', 'id': -1, 'children': {}}

    try:
        with file.open() as fp, tarfile.open(fileobj=fp) as tf:
            # Detect filenames encoding.
            sample = ' '.join(tf.getnames()[:max_files_count])
            if not isinstance(sample, binary_type):
                sample = sample.encode('utf-16be')
            encoding = chardet.detect(sample).get('encoding', 'utf-8')
            for i, info in enumerate(tf.getmembers()):
                if i > max_files_count:
                    raise BufferError('Too many files inside the TAR file.')
                comps = info.name.split(os.sep)
                node = tree
                for c in comps:
                    if not isinstance(c, text_type):
                        c = c.decode(encoding)
                    if c not in node['children']:
                        if c == '':
                            node['type'] = 'folder'
                            continue
                        node['children'][c] = {
                            'name': c,
                            'type': 'item',
                            'id': 'item{0}'.format(i),
                            'children': {}
                        }
                    node = node['children'][c]
                node['size'] = info.size
    except BufferError:
        return tree, True, None
    except (tarfile.ReadError):
        return tree, False, 'Tarfile cannot be read.'
    except Exception as e:
        current_app.logger.warning(str(e), exc_info=True)
        return tree, False, 'Tarfile is not previewable.'

    return tree, False, None


def children_to_list(node):
    """Organize children structure."""
    if node['type'] == 'item' and len(node['children']) == 0:
        del node['children']
    else:
        node['type'] = 'folder'
        node['children'] = list(node['children'].values())
        node['children'].sort(key=lambda x: x['name'])
        node['children'] = map(children_to_list, node['children'])
    return node


def can_preview(file):
    """Return True if filetype can be previewed."""
    supported_extensions = ('.tar', '.gz', '.bz2', '.tgz', '.tbz', '.tbz2')
    return file.is_local() and file.has_extensions(*supported_extensions)


def preview(file):
    """Return appropriate template and pass the file and an embed flag."""
    tree, limit_reached, error = make_tree(file)
    list = children_to_list(tree)['children']
    return render_template(
        "invenio_previewer/zip.html",
        file=file,
        tree=list,
        limit_reached=limit_reached,
        error=error,
        js_bundles=current_previewer.js_bundles + ['previewer_fullscreen_js'],
        css_bundles=current_previewer.css_bundles,
    )
