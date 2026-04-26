from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/rf_prix_final.pkl")
prix_cp = joblib.load("models/prix_cp_mapping.pkl")

@app.post("/predict")
def predict(data: dict):
    surface = data["surface"]
    pieces = data["pieces"]
    code_postal = data["code_postal"]

    prix_moyen_cp = prix_cp.get(code_postal, prix_cp.mean())

    X = pd.DataFrame([{
        "surface_reelle_bati": surface,
        "nombre_pieces_principales": pieces,
        "prix_moyen_cp": prix_moyen_cp
    }])

    pred = model.predict(X)[0]

    return {"prix_estime": round(pred, 0)}
