import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

print("debut du script")
INPUT_PATH = "data/raw/dvf.csv"

chunks = pd.read_csv(
    INPUT_PATH,
    chunksize=100_000,
    low_memory=False
)
print("chunks lus")
df_list = []

for chunk in chunks:
    chunk = chunk[
        (chunk["type_local"] == "Appartement") &
        (chunk["nature_mutation"] == "Vente")
    ]
    print("nouveau chunk traité")
    df_list.append(chunk)

df = pd.concat(df_list, ignore_index=True)
print(df.shape)



#On nettoie notre dataset

#Travail sur la valeur cible (on veut aucune valeur null)
df = df.dropna(subset=["valeur_fonciere"])
#.dropna enlève les valeur nulles sur le subset donné

#on enlève les prix aberrants
df = df[(df["valeur_fonciere"] >= 20000.0) & (df["valeur_fonciere"] <= 5000000.0)]

#on nettoie le nombre de pièces
df=df[(df["nombre_pieces_principales"]>=1)&(df["nombre_pieces_principales"]<=10)]

#on vérifie que numero_disposition (app+cave+parking...) est égal à 1 (on garde que appart)
df=df[(df['numero_disposition']==1)]

#on vérifie que nature_mutation =="Vente" pas d'héritage...
df=df[(df['nature_mutation']=='Vente')]

#On met sous format date et on ne prend que les années >= 2021 (il y a 5 ans max)
df["date_mutation"] = pd.to_datetime(df["date_mutation"])
df = df[df["date_mutation"].dt.year >= 2020]

#le type de code postal est float sauf qu'on veut que ce soit un string d'entier
#donc .astype(int) permet de rendre le float en entier
#.astype(string)le rend en chaine de caractères
df = df.dropna(subset=["code_postal"])
df["code_postal"] = df["code_postal"].astype(int).astype(str)

# on garde seulement les appartements en Ile de France
df = df[
    (df["code_departement"] == 75) |
    (df["code_departement"] == 77) |
    (df["code_departement"] == 78) |
    (df["code_departement"] == 91) |
    (df["code_departement"] == 92) |
    (df["code_departement"] == 93) |
    (df["code_departement"] == 94) |
    (df["code_departement"] == 95)
]




#On détermine les features
df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]
df["annee_vente"] = df["date_mutation"].dt.year

prix_cp = df.groupby("code_postal")["valeur_fonciere"].mean()
df["prix_moyen_cp"] = df["code_postal"].map(prix_cp)

#On garde uniquement les colonnes importantes

COLUMNS_TO_KEEP = [
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "prix_moyen_cp",
    "valeur_fonciere"
]
df = df[(df["prix_m2"] > 1_000) & (df["prix_m2"] < 20_000)]

df = df[COLUMNS_TO_KEEP]



#on entraine notre modèle
from sklearn.ensemble import RandomForestRegressor

X = df[
    [
        "surface_reelle_bati",
        "nombre_pieces_principales",
        "prix_moyen_cp"
    ]
]

y = df["valeur_fonciere"]  # ou prix_m2



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
print("début de l'entrainement")
rf.fit(X_train, y_train)
print("fin de l'entrainement")


from sklearn.metrics import mean_absolute_error

y_pred = rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print("MAE :", mae)
print("Features utilisées :", X.columns)
print("Taille finale :", X.shape)



import joblib
from pathlib import Path

Path("models").mkdir(exist_ok=True)

joblib.dump(rf, "models/rf_prix_final.pkl")
joblib.dump(prix_cp, "models/prix_cp_mapping.pkl")

print("Modèle sauvegardé")
