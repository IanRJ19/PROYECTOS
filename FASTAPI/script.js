const enviar = document.getElementById("enviar");
const resultado = document.getElementById("resultado");

enviar.addEventListener("click", function () {
  const numero = document.getElementById("numero").value;
  fetch(`/adivina/${numero}`)
    .then((res) => res.json())
    .then((data) => {
      resultado.innerHTML = data.resultado;
    });
});
