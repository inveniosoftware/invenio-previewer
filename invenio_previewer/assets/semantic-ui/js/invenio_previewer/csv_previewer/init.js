/*
 * This file is part of Invenio.
 * Copyright (C) 2015-2020 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import $ from "jquery";
import Papa from 'papaparse';

function createDataElement(htmlTag, innerText, parentNode) {
    let node = document.createElement(htmlTag);
    let textnode = document.createTextNode(innerText);
    node.appendChild(textnode);
    parentNode.appendChild(node);
}

var link = "https://" + window.location.host + $("[data-csv-source]").attr('data-csv-source');
var header = true;
var limit = 50;
var step = 0;
var global_parser ;
$("#more_data").click(function () {
  step = 0;
  global_parser.resume();
});


var results = Papa.parse(link, {
  download: true,
  skipEmptyLines: true,
  step: function(row, parser) {
     var element;
     var node = document.createElement("tr");
     if (header) {
        header = false;
        element ="th";
        $("#tableHeader").append(node);
     } else {
        element = "td";
        $("#tableBody").append(node);
     }

     for(let j = 0; j < row.data.length; j++) {
        createDataElement(element, row.data[j], node);
     }
     step++;
     if (step >= limit) {
       parser.pause();
       global_parser = parser;
     }
  },
  complete: function(results) {
     $("#more_data").hide();
  }

});

