const input = document.getElementById("input-enviar");
const fileName = document.querySelector(".file-name");
const enviarButton = document.querySelector(".enviar-button");
const iElement = document.querySelector(".fa-image");
const submitButton = document.querySelector(".submit");

let imageFile;
submitButton.disabled = true;
submitButton.style.cursor = "initial";
submitButton.style.filter = "brightness(50%)";

input.addEventListener("change", (e) => {
  handleFile(e);
});

submitButton.addEventListener("click", () => {
  handleSubmit();
});

async function handleSubmit() {
  const formData = new FormData();
  formData.append("file", imageFile);

  submitButton.disabled = true;
  submitButton.style.cursor = "initial";
  submitButton.style.filter = "brightness(50%)";
  submitButton.textContent = "Enviando...";

  try {
    const response = await fetch("/teste", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const responseObject = await response.json();
      localStorage.setItem("result", responseObject.response);
      localStorage.setItem("accuracy", responseObject.acc);

      window.location.pathname = "/resultado";
    }
  } catch (e) {
    submitButton.disabled = false;
    submitButton.style.cursor = "pointer";
    submitButton.style.filter = "brightness(100%)";
    console.log(e);
  }
}

function handleFile(e) {
  const file = e.target.files[0];
  imageFile = e.target.files[0];
  submitButton.disabled = false;
  submitButton.style.cursor = "pointer";
  submitButton.style.filter = "brightness(100%)";

  enviarButton.style.borderColor = "var(--minBlack)";

  if (file) {
    enviarButton.style.backgroundImage = "none";
    iElement.style.opacity = 0;
  }

  processarImagem(file);
}

function processarImagem(file) {
  const reader = new FileReader();

  reader.onload = function (e) {
    const imagemBase64 = e.target.result;

    enviarButton.style.backgroundImage = `url(${imagemBase64})`;

    enviarButton.style.backgroundSize = "cover";
    enviarButton.style.backgroundPosition = "center";
    enviarButton.style.backgroundRepeat = "no-repeat";
  };

  reader.readAsDataURL(file);
}
