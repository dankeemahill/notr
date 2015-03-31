// Cache jQuery references
var $gallery = null;
var flkty = null;
var decisionSlides = null;


var onDocumentReady = function() {
  // jQuery references
  $gallery = $('.gallery');

  decisionSlides = [3, 9];

  // Initialize
  $gallery.flickity({
    "pageDots": false,
    "accessibility": true,
    "setGallerySize": false,
    "draggable": false
  }).focus();

  flkty = $gallery.data('flickity');

  // Hide flickity buttons on decision slides
  $gallery.on('cellSelect', function() {
    if (decisionSlides.indexOf(flkty.selectedIndex) !== -1) {
      $('.flickity-prev-next-button').hide();
    };
  });

  initButtonEvent();
}

var initButtonEvent = function() {
  $('.decision-btn button').on('click', function() {
    $(this).css('color', '#333');
    var responseText = $('#' + $(this).attr('data-response'))[0].innerHTML;
    $(this).parent()
      .parent()
      .append(responseText);
    $('button', $(this).parent()).off();
    $('.flickity-prev-next-button').show();
  });
}

$(document).ready(onDocumentReady);
