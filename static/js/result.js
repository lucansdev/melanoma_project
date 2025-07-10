const resultHTML = document.querySelector(".result");
const accuracyHTML = document.querySelector(".accuracy");

const result = localStorage.getItem("result");
const accuracy = localStorage.getItem("accuracy");

if (result >= 0.5) {
  resultHTML.innerHTML = "positivo";
} else {
  resultHTML.innerHTML = "negativo";
}

accuracyHTML.innerHTML = `${Number(accuracy).toFixed(2)}`;
