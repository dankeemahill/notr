// Cache jQuery references
var $gallery = null;

var onDocumentReady = function() {
  // jQuery references
  $gallery = $('.gallery');

  // Initialize
  $gallery.flickity({
    "pageDots": false,
    "accessibility": true,
    "setGallerySize": false,
    "draggable": false
  }).focus();

  initButtonEvent();
}

var initButtonEvent = function() {
  $('.decision-btn button').on('click', function() {
    $gallery.flickity('next', true);
  });
}

$(document).ready(onDocumentReady);
