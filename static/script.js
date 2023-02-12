// archivo: static/script.js
document.querySelector("form").addEventListener("submit", function(event) {
    var guess = parseInt(document.querySelector("input[name='guess']").value, 10);
    if (isNaN(guess) || guess < 1 || guess > 100) {
      alert("Por favor, ingrese un número válido entre 1 y 100.");
      event.preventDefault();
    }
  });
  