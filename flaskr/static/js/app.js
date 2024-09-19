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

$(document).ready(function () {
  var socket = io();
  var msgInput = document.getElementById("msg");
  var send = document.getElementById("send");
  var close = document.getElementById("close");
  var output = document.getElementById("output");

  socket.on("my response", function (msg) {
    console.log(msg.time + " -> " + msg.data);
    $("#log").append("<p>" + msg.time + " -> " + msg.data + "</p>");
  });

  send.addEventListener("click", function () {
    var msg = msgInput.value;
    if (msg) {
      socket.emit("message", { msg: msg });
    }
  });

  close.addEventListener("click", function () {
    console.log("close");
    socket.emit("close", {});
  });
});

// window.setInterval(function () {
//   var elem = document.getElementById("log");
//   elem.scrollTop = elem.scrollHeight;
// }, 200);
