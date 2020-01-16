$(document).ready(function () {
    $('.overlay').on('click', function () {
        $('#sidebar').toggleClass('active');
        $('.overlay').toggleClass('active');
    });

    $('#sidebarToggle').on('click', function () {
        $('#sidebar').toggleClass('active');
        $('.overlay').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });

    var scrollTop = $(".scroll-to-top");

    $("#body").scroll(function() {
      // declare variable
      var topPos = $(this).scrollTop();

      // if user scrolls down - show scroll to top button
      if (topPos > 100) {
        $(scrollTop).css("opacity", "1");

      } else {
        $(scrollTop).css("opacity", "0");
      }

    }); // scroll END

    $(scrollTop).click(function(){
      $('#body').animate({
          scrollTop: 0
      }, 500);
      });
});
