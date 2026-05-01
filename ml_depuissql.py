import pandas as pd
import random
from faker import Faker

fake = Faker("fr_FR")

services = ["RH", "Finance", "Qualité", "Informatique", "Commercial"]
statuts = ["À jour", "À réviser", "Obsolète"]

data = []

for i in range(1, 101):
    date_creation = fake.date_between(start_date="-3y", end_date="-6m")
    date_maj = fake.date_between(start_date=date_creation, end_date="today")

    data.append({
        "ID_document": i,
        "Nom_document": f"Document_{i}",
        "Service": random.choice(services),
        "Responsable": fake.name(),
        "Date_creation": date_creation,
        "Date_mise_a_jour": date_maj,
        "Statut": random.choice(statuts)
    })

df = pd.DataFrame(data)

df["Date_mise_a_jour"] = pd.to_datetime(df["Date_mise_a_jour"])
df["Jours_depuis_maj"] = (pd.Timestamp.today() - df["Date_mise_a_jour"]).dt.days

df["Document_en_retard"] = df["Jours_depuis_maj"].apply(
    lambda x: "Oui" if x > 365 else "Non"
)

df.to_excel("base_documents.xlsx", index=False)

print("Base créée avec succès : base_documents.xlsx")