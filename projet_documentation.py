import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

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

df = pd.read_sql("SELECT * FROM documents", engine)

df_ml = df.copy()

le_service = LabelEncoder()
le_statut = LabelEncoder()

df_ml["service_encoded"] = le_service.fit_transform(df_ml["service"])
df_ml["statut_encoded"] = le_statut.fit_transform(df_ml["statut"])

df_ml["retard_encoded"] = df_ml["document_en_retard"].map({
    "Non": 0,
    "Oui": 1
})

X = df_ml[[
    "service_encoded",
    "statut_encoded",
    "jours_depuis_maj"
]]

y = df_ml["retard_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
score = accuracy_score(y_test, y_pred)

print("Score du modèle :", round(score * 100, 2), "%")

df["risque_retard"] = model.predict(X)

df["risque_retard"] = df["risque_retard"].map({
    0: "Faible",
    1: "Élevé"
})

df.to_sql("documents", engine, if_exists="replace", index=False)

df.to_excel("base_documents_finale.xlsx", index=False)

print("ML terminé : risques sauvegardés dans PostgreSQL et Excel.")