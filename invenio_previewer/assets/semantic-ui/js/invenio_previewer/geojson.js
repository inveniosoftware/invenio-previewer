/*
 * This file is part of Invenio.
 * Copyright (C) 2015-2024 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import L from "leaflet"
import "leaflet/dist/leaflet.css";

document.addEventListener("DOMContentLoaded", () => {
  const mapElement = document.getElementById('map')
  const fileUri = mapElement.getAttribute('data-file-uri')
  const fileUrl = new URL(fileUri, window.location.href);

  const map = L.map('map').setView([0, 0], 13);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  fetch(fileUrl.href).then(res => res.json()).then(data => {
    const geoJsonLayer = L.geoJson(data, {
      style: {
        color: "#3399ff",
        weight: 2,
        opacity: 0.5
      },
      pointToLayer: (feature, latlng) => L.circleMarker(latlng, {
        radius: 4,
        fillColor: "#3399ff",
        color: "#3399ff",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
      })
    })
    geoJsonLayer.addTo(map);
    map.fitBounds(geoJsonLayer.getBounds());
  });
});
