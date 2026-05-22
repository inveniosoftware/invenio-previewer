/*
 * SPDX-FileCopyrightText: 2015-2020 CERN.
 * SPDX-License-Identifier: MIT
 */

import $ from "jquery";

$(".ui.button.embed-btn").click(function () {
  $("#embedModal").modal("show");
});

$("#close-btn").click(function () {
  $("#embedModal").modal("hide");
});
