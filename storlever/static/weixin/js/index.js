$(function(){
  $('.preview-play img').click(function(event) {
    /* Act on the event */
    var el = $(this).parents('.preview').find('.preview-img img');
    var pc = $('#player-container').width(el.width()).height(el.height()).css({'visibility': 'visible'});
    var p  = videojs('player');
    p.width(el.width());
    p.height(el.height());
    var offset = el.offset();
    pc.offset(offset);
    p.play();
  });
});