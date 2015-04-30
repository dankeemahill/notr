// Cache jQuery references
var $gallery = null;
var flkty = null;


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

  flkty = $gallery.data('flickity');

  $gallery.on('cellSelect', function() {
    var flickIndex = flkty.selectedIndex;

    switch (flickIndex) {
      case 2:
      case 4:
        // Autoplay videos on video slides
        $('video', $('.content')[flickIndex])[0].play();
        break;
      case 3:
      case 9:
        // Hide flickity buttons on decision slides
        $('.flickity-prev-next-button').hide();
        break;
    }
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
