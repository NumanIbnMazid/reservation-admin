// dynamic navbar active
$(function ($) {
    let url = window.location.href;
    $('nav ul li a').each(function () {
        if (this.href === url) {
            $(this).addClass('active');
            $(this).parent().parent().parent().addClass('menu-open');
        }
    });

    // console.log(url);
});

// generate group add url
$(function ($) {
    let base_url = window.location.origin;
    let group_add_endpoint = "/admin/auth/group/add/";
    let group_add_url = base_url + group_add_endpoint;

    // console.log(group_add_url);
    $("#user-group-add-ref").attr("href", group_add_url);
});


// scroll to top
$(window).scroll(function() {
  if ($(this).scrollTop() > 300) {
    $(".auto-scroll-to-top").addClass("visible");
  } else {
    $(".auto-scroll-to-top").removeClass("visible");
  }
});

$(".auto-scroll-to-top").click(function() {
  $("html, body").animate({ scrollTop: 0 }, 600);
});

// go back button
$("button#go_back").on("click", function(e) {
  e.preventDefault();
  window.history.back();
});


// ripple-effect
$('button, .menu a, .to-ripple').rippleEffect();

// accordian JS ==========================
$(document).ready(function () {
  $('.accordian-card-heading').on('click', function () {
    if ($(this).parents('.accordian-card').hasClass('open')) {
      $(this).parents('.accordian-card').find('.accordian-card-body').slideUp();
      $(this).parents('.accordian-card').removeClass('open');
    } else {
      $('.accordian-card-body').slideUp();
      $('.accordian-card').removeClass('open');

      $(this).parents('.accordian-card').find('.accordian-card-body').slideDown();
      $(this).parents('.accordian-card').addClass('open');
    }
  });
});