var THEMETAGS = THEMETAGS || {};

(function () {
  'use strict'; //preloader

  $(window).ready(function () {
    $('#preloader').delay(100).fadeOut('fade');
  }); //dropdown menu hover js

  $('ul.nav li.dropdown').hover(function () {
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(200);
  }, function () {
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(200);
  }); //sticky header

  $(window).on('scroll', function () {
    var scroll = $(window).scrollTop();

    if (scroll < 2) {
      $('nav.sticky-header').removeClass('affix');
    } else {
      $('nav.sticky-header').addClass('affix');
    }
  }); //swiper slide js

  var swiper = new Swiper('.testimonialSwiper', {
    slidesPerView: 2,
    speed: 700,
    spaceBetween: 30,
    slidesPerGroup: 2,
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1
      },
      640: {
        slidesPerView: 1
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 20
      },
      1024: {
        slidesPerView: 2,
        spaceBetween: 25
      },
      1142: {
        slidesPerView: 2,
        spaceBetween: 30
      }
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    }
  }); //app two review slider

  var swiper = new Swiper('.appTwoReviewSwiper', {
    slidesPerView: 2,
    speed: 700,
    spaceBetween: 30,
    slidesPerGroup: 2,
    loop: true,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 30
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 30
      },
      991: {
        slidesPerView: 3,
        spaceBetween: 30
      }
    }
  });
  THEMETAGS.initialize = {
    init: function () {
      THEMETAGS.initialize.general();
    },
    general: function () {
      // Mouse Move Parallax Element
      var $scene = $('.parallax-element').parallax({
        scalarX: 100,
        scalarY: 100
      });
    }
  };
  THEMETAGS.documentOnReady = {
    init: function () {
      THEMETAGS.initialize.init();
    }
  };
  $(document).ready(THEMETAGS.documentOnReady.init);
  $(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
  }); //animated js

  AOS.init({
    easing: 'ease-in-out',
    // default easing for AOS animations
    once: true,
    // whether animation should happen only once - while scrolling down
    duration: 500 // values from 0 to 3000, with step 50ms

  }); //magnific popup js

  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false
  });
  $('.popup-with-form').magnificPopup({
    type: 'inline',
    preloader: false,
    focus: '#name'
  });
})();