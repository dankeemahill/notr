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
    var content = $(this).parent().parent();

    var responseText = $('#' + $(this).attr('data-response'))[0].innerHTML;
    responseText = $(responseText).attr('class', 'response-text');

    // Remove response text if making second decision
    if ($('.response-text', content).length) {
      $('.response-text', content).remove();
    }

    content.append(responseText);

    $('.flickity-prev-next-button').show();
  });
}

$(document).ready(onDocumentReady);
