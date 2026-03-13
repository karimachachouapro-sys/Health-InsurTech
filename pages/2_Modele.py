import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

st.title("📈 Modélisation & Analyse des Biais")

st.write("""
Cette page permet d'entraîner un modèle de **régression linéaire**
pour prédire les frais médicaux à partir des caractéristiques des patients.
""")

# Charger dataset
csv_path = os.path.join(os.path.dirname(__file__), "..", "insurance_data.csv")
df = pd.read_csv(csv_path)



# Bouton pour entraîner le modèle
if st.button("🚀 Entraîner le modèle de régression"):

    # -------------------------
    # Préparation des données
    # -------------------------
    df['sex'] = df['sex'].map({'male': 0, 'female': 1})
    df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})

    le = LabelEncoder()
    df['mutuelle_complementaire'] = le.fit_transform(df['mutuelle_complementaire'])

    df = df.dropna(subset=['age','sex','bmi','children','smoker','mutuelle_complementaire','charges'])

    features = ['age','sex','bmi','children','smoker','mutuelle_complementaire']
    target = 'charges'

    X = df[features]
    y = df[target]

    # -------------------------
    # Split train / test
    # -------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    # -------------------------
    # Entraîner modèle
    # -------------------------
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # -------------------------
    # Évaluation
    # -------------------------
    rmse = np.sqrt(mean_squared_error(y_test,y_pred))
    r2 = r2_score(y_test,y_pred)

    st.subheader("📊 Performance du modèle")

    col1, col2 = st.columns(2)

    col1.metric("RMSE", f"{rmse:.2f}")
    col2.metric("R²", f"{r2:.2f}")

    # -------------------------
    # Coefficients
    # -------------------------
    st.subheader("📈 Coefficients du modèle")

    coeff = pd.DataFrame({
        'Variable': features,
        'Coefficient': model.coef_
    })

    st.dataframe(coeff)

    # -------------------------
    # Analyse des biais
    # -------------------------
    df_test = X_test.copy()
    df_test['charges_pred'] = y_pred
    df_test['smoker_label'] = df_test['smoker'].map({0:'Non',1:'Oui'})
    df_test['sex_label'] = df_test['sex'].map({0:'Homme',1:'Femme'})

    st.subheader("Analyse des biais")

    st.write("Prédiction moyenne par catégorie fumeur/non-fumeur")
    st.dataframe(df_test.groupby('smoker_label')['charges_pred'].mean())

    st.write("Prédiction moyenne par sexe")
    st.dataframe(df_test.groupby('sex_label')['charges_pred'].mean())

    st.success("Modèle entraîné avec succès ✔")
