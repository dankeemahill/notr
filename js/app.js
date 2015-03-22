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
    $(this).css('color', '#333');
    var responseText = $('#' + $(this).attr('data-response'))[0].innerHTML;
    $(this).parent()
      .parent()
      .append(responseText);
    $('button', $(this).parent()).off()
  });
}

$(document).ready(onDocumentReady);
