# modele_etape2_final.py
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from logger import logger

logger.info("Entraînement du modèle lancé")

# 1️⃣ Charger le dataset
csv_path = os.path.join(os.path.dirname(__file__), "..", "insurance_data.csv")
df = pd.read_csv(csv_path)

# 2️⃣ Vérification rapide des valeurs uniques
print("Valeurs uniques dans 'sex' :", df['sex'].unique())
print("Valeurs uniques dans 'smoker' :", df['smoker'].unique())
print("Valeurs uniques dans 'mutuelle_complementaire' :", df['mutuelle_complementaire'].unique())

# 3️⃣ Conversion des colonnes catégorielles
df['sex'] = df['sex'].map({'male': 0, 'female': 1})
df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})

# Pour mutuelle_complementaire : transformer en label numérique
le = LabelEncoder()
df['mutuelle_complementaire'] = le.fit_transform(df['mutuelle_complementaire'])

# 4️⃣ Supprimer les lignes avec NaN restantes
df = df.dropna(subset=['age', 'sex', 'bmi', 'children', 'smoker', 'mutuelle_complementaire', 'charges'])

# 5️⃣ Définir les features et la cible
features = ['age', 'sex', 'bmi', 'children', 'smoker', 'mutuelle_complementaire']
target = 'charges'
X = df[features]
y = df[target]

# 6️⃣ Séparer train et test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7️⃣ Entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# 8️⃣ Évaluer le modèle
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.2f}")
r2 = r2_score(y_test, y_pred)
print(f"\nRMSE: {rmse:.2f}")
print(f"R²: {r2:.2f}")

# 9️⃣ Afficher les coefficients
coefficients = pd.DataFrame({'Variable': features, 'Coefficient': model.coef_})
print("\nCoefficients du modèle :")
print(coefficients)

# 🔹 Analyse des biais : smoker
df_test = X_test.copy()
df_test['charges_pred'] = y_pred
df_test['smoker_label'] = df_test['smoker'].map({0: 'Non', 1: 'Oui'})
mean_charges_smoker = df_test.groupby('smoker_label')['charges_pred'].mean()
print("\nPrédiction moyenne par catégorie fumeur/non-fumeur :")
print(mean_charges_smoker)

# 🔹 Analyse des biais : sex
df_test['sex_label'] = df_test['sex'].map({0: 'Homme', 1: 'Femme'})
mean_charges_sex = df_test.groupby('sex_label')['charges_pred'].mean()
print("\nPrédiction moyenne par sexe :")
print(mean_charges_sex)

# 🔹 Proposition pour atténuer le biais
print("\n💡 Proposition : rééchantillonner ou normaliser les données pour réduire l'effet disproportionné des catégories sensibles (smoker ou sex).")