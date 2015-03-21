// Cache jQuery references
var $gallery = null;

var onDocumentReady = function() {
  // jQuery references
  $gallery = $('.gallery');

  // Initialize
  $gallery.flickity({
    "pageDots": false,
    "accessibility": true,
    "setGallerySize": false
  }).focus();
}

$(document).ready(onDocumentReady);
