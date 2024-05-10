// This file is part of InvenioRDM
// Copyright (C) 2024 CERN.
//
// Invenio Theme TUW is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

window.WORKER_SRC = "/static/js/pdfjs/pdf.worker.js') }}";
document.addEventListener("DOMContentLoaded", () => {
    const pdfURL = document.getElementById("pdf-file-uri").value;
    window.PDFViewerApplication.open({"url": pdfURL});
});
