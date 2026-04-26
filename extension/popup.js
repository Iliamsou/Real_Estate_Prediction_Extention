let appartementData = null;

document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("appartementData", (result) => {
    if (!result.appartementData) {
      document.getElementById("info").innerText =
        "Annonce non compatible (pas appartement IDF)";
      return;
    }

    appartementData = result.appartementData;

    document.getElementById("info").innerText =
      `Surface : ${appartementData.surface} m²
Pièces : ${appartementData.pieces}
Code postal : ${appartementData.code_postal}`;

    document.getElementById("estimate").style.display = "block";
  });
});

document.getElementById("estimate").addEventListener("click", () => {
  if (!appartementData) return;

  fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      surface: appartementData.surface,
      pieces: appartementData.pieces,
      code_postal: appartementData.code_postal
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText =
        `Prix estimé : ${data.prix_estime} €`;
    })
    .catch(() => {
      document.getElementById("result").innerText =
        "Erreur lors de l'estimation";
    });
});
