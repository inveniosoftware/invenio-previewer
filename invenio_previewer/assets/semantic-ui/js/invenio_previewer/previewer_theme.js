/*
 * SPDX-FileCopyrightText: 2020 CERN.
 * SPDX-License-Identifier: MIT
 */

// eslint-disable-next-line no-unused-vars
import jquery from "jquery/dist/jquery";
import "semantic-ui-css/semantic.js";
import "semantic-ui-less/semantic.less";

// Initialize Semantic UI components
jquery(document).ready(function () {
  jquery(".question.circle.checksum.icon").popup();
});
