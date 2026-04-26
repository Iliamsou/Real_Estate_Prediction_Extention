(function () {

  console.log("content.js chargé");

  if (!window.location.href.includes("/ad/ventes_immobilieres")) {
    console.log("Pas une annonce immo");
    return;
  }

  console.log("Annonce immobilière détectée");

  function getTextByQaId(qaId) {
    const el = document.querySelector(`[data-qa-id="${qaId}"]`);
    return el ? el.innerText.trim() : null;
  }

  function extractCodePostal(text) {
    const match = text.match(/\((\d{5})\)/);
    return match ? match[1] : null;
  }

  const typeBien = getTextByQaId("criteria_item_real_estate_type");
  const surfaceText = getTextByQaId("criteria_item_square");
  const piecesText = getTextByQaId("criteria_item_rooms");

  const locationBlock = document.querySelector('[data-test-id="location-map-title"]');
  const locationText = locationBlock
    ? locationBlock.querySelectorAll("p")[1]?.innerText
    : null;

  console.log("Type :", typeBien);
  console.log("Surface :", surfaceText);
  console.log("Pièces :", piecesText);
  console.log("Localisation :", locationText);

  if (!typeBien || !typeBien.toLowerCase().includes("appartement")) {
    console.log("Pas un appartement");
    return;
  }

  const surface = surfaceText ? parseFloat(surfaceText.replace(",", ".")) : null;
  const pieces = piecesText ? parseInt(piecesText) : null;
  const code_postal = locationText ? extractCodePostal(locationText) : null;

  if (!surface || !pieces || !code_postal) {
    console.log("Infos manquantes");
    return;
  }

  const departement = parseInt(code_postal.substring(0, 2));
  const IDF = [75, 77, 78, 91, 92, 93, 94, 95];

  if (!IDF.includes(departement)) {
    console.log("Pas en Île-de-France");
    return;
  }

  console.log("Appartement IDF valide");

  const appartementData = {
    surface,
    pieces,
    code_postal
  };

  chrome.storage.local.set({ appartementData }, () => {
    console.log("Données sauvegardées :", appartementData);
  });

  chrome.runtime.sendMessage(appartementData);

})();
