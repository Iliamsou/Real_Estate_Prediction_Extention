(function () {

  console.log("content.js chargé");

  if (!window.location.href.includes("/ad/ventes_immobilieres")) {
    console.log("Pas une annonce immobilière");
    return;
  }

  console.log("Annonce immobilière détectée");


  function getTextByQaId(qaId) {
    const el = document.querySelector(`[data-qa-id="${qaId}"]`);
    return el ? el.innerText.trim() : null;
  }

  function extractCodePostalFromAria() {
    const link = document.querySelector(
      'a[aria-label*="," i]'
    );

    if (!link) return null;

    const aria = link.getAttribute("aria-label");
    console.log("aria-label trouvé :", aria);

    const match = aria.match(/\b\d{5}\b/);
    return match ? match[0] : null;
  }

  function extractNumber(text) {
  if (!text) return null;
  const match = text.match(/(\d+([.,]\d+)?)/);
  return match ? parseFloat(match[1].replace(",", ".")) : null;
}

function extractInt(text) {
  if (!text) return null;
  const match = text.match(/\d+/);
  return match ? parseInt(match[0]) : null;
}



  const typeBien = getTextByQaId("criteria_item_real_estate_type");
  const surfaceText = getTextByQaId("criteria_item_square");
  const piecesText = getTextByQaId("criteria_item_rooms");
  const codePostal = extractCodePostalFromAria();

  console.log("Type :", typeBien);
  console.log("Surface :", surfaceText);
  console.log("Pièces :", piecesText);
  console.log("Code postal extrait :", codePostal);


  if (!typeBien || !typeBien.toLowerCase().includes("appartement")) {
    console.log("Pas un appartement");
    return;
  }

  const surface = extractNumber(surfaceText);
  const pieces = extractInt(piecesText);


  if (!surface || !pieces || !codePostal) {
    console.log("Infos manquantes");
    return;
  }

  const departement = codePostal.substring(0, 2);

  const IDF = ["75", "77", "78", "91", "92", "93", "94", "95"];

  console.log("Département détecté :", departement);

  if (!IDF.includes(departement)) {
    console.log("Pas en Île-de-France");
    return;
  }

  console.log("Appartement IDF valide");


  const appartementData = {
    surface,
    pieces,
    code_postal: codePostal
  };

  chrome.storage.local.set({ appartementData }, () => {
    console.log("Données sauvegardées :", appartementData);
  });

  chrome.runtime.sendMessage(appartementData);

})();
