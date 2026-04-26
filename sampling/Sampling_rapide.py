import pandas as pd

INPUT_PATH = "dvf.csv.gz"
OUTPUT_PATH = "dvf_idf_sample.csv"

# Départements IDF (via code postal)
IDF_DEPARTMENTS = {"75", "77", "78", "91", "92", "93", "94", "95"}

# Colonnes MINIMALES à lire
COLUMNS_TO_KEEP = [
    "date_mutation",
    "nature_mutation",
    "valeur_fonciere",
    "numero_disposition",
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "code_postal",
    "type_local"
]

TARGET_ROWS = 30_000
current_rows = 0
first_chunk = True

chunks = pd.read_csv(
    INPUT_PATH,
    compression="gzip",
    usecols=COLUMNS_TO_KEEP,
    chunksize=100_000,
    low_memory=False
)

for chunk in chunks:
    # Créer le département à partir du code postal
    chunk["code_departement"] = chunk["code_postal"].astype(str).str[:2]

    # Filtrage métier
    chunk = chunk[
        (chunk["nature_mutation"] == "Vente") &
        (chunk["numero_disposition"] == 1) &
        (chunk["type_local"] == "Appartement") &
        (chunk["code_departement"].isin(IDF_DEPARTMENTS))
    ]

    if chunk.empty:
        continue

    remaining = TARGET_ROWS - current_rows
    if remaining <= 0:
        break

    chunk = chunk.head(remaining)

    chunk.to_csv(
        OUTPUT_PATH,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    current_rows += len(chunk)
    first_chunk = False

    print(f"➡️ {current_rows} lignes collectées")

print(f"\n Échantillon final créé : {current_rows} lignes")
