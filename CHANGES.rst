..
    This file is part of Invenio.
    Copyright (C) 2016-2025 CERN.
    Copyright (C) 2024-2025 Graz University of Technology.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Changes
=======

Version v3.4.0 (released 2025-10-08)

- feat(warc): new Web Archive previewer

Version v3.3.0 (released 2025-08-25)

- fix(ext): avoid unecessary assert error
    * The check for an already registered previewer was just checking by
      name, instead of also verifying if the registered object is the same
      instance.
    * Instead of an assertion, we raise a `RuntimeError` with information
      about the already registered and conflicting previewer instances.
- feat(pdfjs): open links in new tabs
    * Sets by default in the PDF.js settings that links open in a new tab.
      The old behaviort was that when clicking a link inside a previewed
      PDF, the navigation happens inside the iframe, which then because of
      the `X-Frame-Options: sameorigin` setting blocked the content.
- feat(pdfjs): disable sandboxed JS execution by default
    * Adds a new `PREVIEWER_PDF_JS_ENABLE_SCRIPTING` config variable for
      allowing to disable the sandboxed JS execution support in PDF.js.
      This config is by default set to `False`.
- file-list: show fallback message if file checksum is not available

Version v3.2.0 (released 2025-07-17)

- i18n: pulled translations

Version 3.1.0 (release 2025-07-02)

- fix(tests): add missing javascript dep
- fix: pkg_resources DeprecationWarning
- docs: add webp to all places formats are listed
- feat: preview webp images
- i18n: removed deprecated messages
- fix: setuptools require underscores instead of dashes
- csv: add max filesize check

Version 3.0.1 (release 2025-02-25)

- fix: ModuleWarning: Deprecation Warning

Version 3.0.0 (release 2024-12-10)

- fix: tests, compatibility with sqlalchemy>=2
- setup: bump major dependencies

Version 2.3.0 (released 2024-12-10)

- zip: move fullscreen.js to fix the zip previewer
- pdfjs: upgrade to pdf.js v4

Version 2.2.2 (release 2024-11-30)

- setup: change to reusable workflows
- setup: pin dependencies
- i18n:push translations

Version 2.2.0 (released 2024-03-26)
-----------------------------------

- integrated new video/audio previewer

Version 2.1.2 (released 2024-03-12)
-----------------------------------

- frontend: Improve display of ZIPs with long file names

Version 2.1.1 (released 2024-01-31)
-----------------------------------

- markdown: default message if not previewable
- markdown: fixed ascii encoding typo

Version 2.1.0 (Release 2023-12-05)
----------------------------------

- setup: migrate dependency from cchardet to charset_normalizer
  fixes problems with python3.11
- setup: add python3.11 to test matrix

Version 2.0.2 (Release 2023-11-20)
----------------------------------

- CSV: Fix handling of small files.

Version 2.0.1 (Release 2023-09-14)
----------------------------------

- CSV: removed file size limit. The new extension can preview very large files.

Version 2.0.0 (Release 2023-09-14)
----------------------------------

- CSV: change JS rendering from `d3` to `papaparse`, supporting rendering
  of very large files
- add file size check to CSV extensions
- refactor XML and ipynb extensions

Version 1.5.0 (Release 2023-08-17)
----------------------------------

- encoding: cleanup detection and override ASCII to default encoding
- txt-preview: enables horizontal scrolling, avoid invalid coding errors and add
  option to truncate .txt file preview after `PREVIEWER_TXT_MAX_BYTES`
- pull latest translations

Version 1.4.0 (Release 2023-03-02)
----------------------------------

- remove deprecated flask_babelex dependency
- upgrade invenio_i18n

Version 1.3.9 (Release 2023-01-13)
----------------------------------

- remove inline script - pdf js

Version 1.3.8 (Release 2022-11-18)
----------------------------------
- add translations

Version 1.3.7 (Release 2022-09-05)
----------------------------------

- jupyter: fix previewer of jpynb
- tests: upgrade invenio-db

Version 1.3.6 (Release 2022-03-31)
----------------------------------

- Fix dependencies

Version 1.3.5 (Release 2022-02-28)
----------------------------------

- Align bootstrap-sass version with Invenio-Theme version.

Version 1.3.3 (Release 2021-07-12)
------------------------------------

- Adds german translations


Version 1.3.2 (Release 2020-12-11)
------------------------------------

- Fixes the preview button and the question icon mark in the Jinja macro.

Version 1.3.1 (Release 2020-12-11)
------------------------------------

- Fixes the file download link the Jinja macro for listing files.

Version 1.3.0 (Release 2020-12-10)
------------------------------------

- Migration to Semantic-UI.
- Drops support of flask-assets.
- Fixes PDF.js static asset paths.
- Migrate CI to GitHub Actions.
- Fixes imports in Bootstrap and Semantic UI files.

Version 1.2.1 (Release 2020-05-07)
----------------------------------

- set Sphinx ``<3`` because of errors related to application context
- stop using example app

Version 1.2.0 (Release 2020-03-13)
----------------------------------

- Change flask dependency to centrally managed by invenio-base
- Drop support for Python 2.7

Version 1.1.0 (Release 2019-12-20)
----------------------------------

- Changes styling and method signature of file_list macro.

Version 1.0.2 (Release 2019-11-21)
----------------------------------

- Removes inline styling from simple image previewer for Content Security
  Policy compliance

Version 1.0.1 (Release 2019-08-02)
----------------------------------

- Removes html sanitization config

Version 1.0.0 (release 2019-07-29)
----------------------------------

- Initial public release.
