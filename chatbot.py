import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_USER = "postgres"
DB_PASSWORD = "Cspuc2334@2003!"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "gestion_documentaire"

url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(url)

df = pd.read_excel("base_documents.xlsx")

df = df.rename(columns={
    "ID_document": "id_document",
    "Nom_document": "nom_document",
    "Service": "service",
    "Responsable": "responsable",
    "Date_creation": "date_creation",
    "Date_mise_a_jour": "date_mise_a_jour",
    "Statut": "statut",
    "Jours_depuis_maj": "jours_depuis_maj",
    "Document_en_retard": "document_en_retard"
})

df["risque_retard"] = None

df.to_sql("documents", engine, if_exists="append", index=False)

print(" Données envoyées vers PostgreSQL avec succès !")