/* Copyright 2014 Mozilla Foundation
 * Copyright 2024 TU Wien
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const { pdfjsLib, pdfjsViewer } = window;

  // The workerSrc property shall be specified
  pdfjsLib.GlobalWorkerOptions.workerSrc = "/static/js/pdfjs/build/pdf.worker.min.mjs";

  // Some PDFs need external cmaps
  const CMAP_URL = "/static/js/pdfjs/cmaps/";
  const CMAP_PACKED = true;

  // Get the PDF file's URL
  const PDF_URL = document.getElementById("pdf-file-uri").value;
  const ENABLE_XFA = true;

  const SANDBOX_BUNDLE_SRC = "/static/js/pdfjs/build/pdf.sandbox.min.mjs";

  const container = document.getElementById("viewerContainer");
  const nextPageButton = document.getElementById("next");
  const prevPageButton = document.getElementById("previous");
  const pageNumberField = document.getElementById("pageNumber");
  const pageNumberLabel = document.getElementById("numPages");
  const zoomInButton = document.getElementById("zoomInButton");
  const zoomOutButton = document.getElementById("zoomOutButton");
  const scaleSelect = document.getElementById("scaleSelect");

  const eventBus = new pdfjsViewer.EventBus();

  // (Optionally) enable hyperlinks within PDF files
  const pdfLinkService = new pdfjsViewer.PDFLinkService({
    eventBus,
  });

  // (Optionally) enable find controller
  const pdfFindController = new pdfjsViewer.PDFFindController({
    eventBus,
    linkService: pdfLinkService,
  });

  // (Optionally) enable scripting support
  const pdfScriptingManager = new pdfjsViewer.PDFScriptingManager({
    eventBus,
    sandboxBundleSrc: SANDBOX_BUNDLE_SRC,
  });

  const pdfViewer = new pdfjsViewer.PDFViewer({
    container,
    eventBus,
    linkService: pdfLinkService,
    findController: pdfFindController,
    scriptingManager: pdfScriptingManager,
  });
  pdfLinkService.setViewer(pdfViewer);
  pdfScriptingManager.setViewer(pdfViewer);

  // Register event handlers for controls
  nextPageButton.addEventListener("click", function() {
    pdfViewer.nextPage();
    pageNumberField.value = pdfViewer.currentPageNumber;
  });
  prevPageButton.addEventListener("click", function() {
    pdfViewer.previousPage();
    pageNumberField.value = pdfViewer.currentPageNumber;
  });
  pageNumberField.addEventListener("change", function(e) {
    let pageNumber = parseInt(e.target.value);
    if (pageNumber > pdfViewer.pagesCount) {
      pageNumber = pdfViewer.pagesCount;
    } else if (pageNumber < 1) {
      pageNumber = 1;
    }
    pdfViewer.currentPageNumber = pageNumber;
    pageNumberField.value = pageNumber;
  });
  zoomInButton.addEventListener("click", function() {
    pdfViewer.increaseScale();
  });
  zoomOutButton.addEventListener("click", function() {
    pdfViewer.decreaseScale();
  });
  scaleSelect.addEventListener("change", function(e) {
    pdfViewer.currentScaleValue = e.target.value;
  });

  // Register event handlers on the event bus
  eventBus.on("pagechanging", function(e) {
    pageNumberField.value = e.pageNumber;
  });
  eventBus.on("scalechanging", function(e) {
    // When the scale changes, make sure the appropriate option is selected
    // in the dropdown UI (if no match can be found, the invalid index is fine)
    let idx = -1;
    for (let i = 0; i < scaleSelect.options.length; i++) {
      const option = scaleSelect.options[i];

      // `e.presetValue` has string values like "auto" or "page-fit",
      // while `e.scale` has numeric values like 1.25
      if (e.presetValue == option.value || e.scale == option.value) {
        idx = i;
        break;
      }
    }
    scaleSelect.selectedIndex = idx;
  });
  eventBus.on("pagesinit", function () {
    // We can use pdfViewer now, e.g. let's change default scale
    pdfViewer.currentScaleValue = "auto";

    // Display the number of pages
    pageNumberLabel.textContent = `of ${pdfViewer.pagesCount}`;
  });

  // Loading document
  const loadingTask = pdfjsLib.getDocument({
    url: PDF_URL,
    cMapUrl: CMAP_URL,
    cMapPacked: CMAP_PACKED,
    enableXfa: ENABLE_XFA,
  });
  (async function () {
    const pdfDocument = await loadingTask.promise;

    // Document loaded, specifying document for the viewer and the (optional) linkService
    pdfViewer.setDocument(pdfDocument);
    pdfLinkService.setDocument(pdfDocument, null);
  })();
});
