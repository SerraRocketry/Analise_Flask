$(document).ready(function () {
  // Toggle do menu hamburger
  $(".humbarger").click(function (event) {
    $(".menu-list").slideToggle(500); // Alterna o menu com animação
    event.preventDefault();
  });

  // Fecha o menu quando um link é clicado (somente para telas pequenas)
  $(".menu-list li a").click(function (event) {
    if ($(window).width() < 768) {
      $(".menu-list").slideUp(500); // Fecha o menu após clicar no link
    }
  });
});

