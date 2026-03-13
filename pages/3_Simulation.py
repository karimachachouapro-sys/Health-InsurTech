import streamlit as st
import pandas as pd
import altair as alt
import os
from sklearn.preprocessing import LabelEncoder
from src.modele import model
from logger import logger

logger.info("Simulation réalisée par un utilisateur")

st.title("🧾 Simulation de vos charges")

# Charger dataset pour LabelEncoder
csv_path = os.path.join(os.path.dirname(__file__), "..", "insurance_data.csv")
df = pd.read_csv(csv_path)
le = LabelEncoder()
le.fit(df['mutuelle_complementaire'])

# Formulaire utilisateur
age = st.number_input("Âge", min_value=0, max_value=120, value=30)
sex = st.selectbox("Sexe", ['male','female'])
smoker = st.selectbox("Fumeur ?", ['yes','no'])

# IMC : si l'utilisateur ne le connaît pas
use_calc = st.checkbox("Je veux calculer mon IMC")
if use_calc:
    poids = st.number_input("Poids (kg)", min_value=0.0)
    taille = st.number_input("Taille (m)", min_value=0.0)
    bmi = round(poids / (taille**2),2) if taille > 0 else 0
else:
    bmi = st.number_input("IMC", min_value=0.0, value=22.0)

children = st.number_input("Nombre d'enfants", min_value=0, max_value=10, value=0)
mutuelle = st.selectbox("Mutuelle", df['mutuelle_complementaire'].unique())

# Bouton prédire
if st.button("Calculer mes charges"):
    sex_val = 0 if sex=='male' else 1
    smoker_val = 1 if smoker=='yes' else 0
    mutuelle_val = le.transform([mutuelle])[0]
    
    X_user = pd.DataFrame([[age, sex_val, bmi, children, smoker_val, mutuelle_val]],
                          columns=['age','sex','bmi','children','smoker','mutuelle_complementaire'])
    
    charges_pred = model.predict(X_user)[0]
    st.success(f"💰 Vos charges annuelles estimées : {charges_pred:.2f} €")
