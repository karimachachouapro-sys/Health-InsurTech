# streamlit_app_data.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.title("📊 Exploration des données")

# Charger le dataset
csv_path = os.path.join(os.path.dirname(__file__), "..", "insurance_data.csv")
df = pd.read_csv(csv_path)

# -----------------------------
# Statistiques descriptives
# -----------------------------
st.subheader("Statistiques descriptives")
st.write("Résumé statistique du dataset :")
st.dataframe(df.describe())

# -----------------------------
# Dashboard interactif
# -----------------------------
st.subheader("Dashboard : corrélation entre l'âge, l'IMC et les frais médicaux")
st.write("""
Ce graphique montre la relation entre :
- **Âge**
- **IMC**
- **Frais médicaux**
- **Statut fumeur** (couleur)
""")

# -----------------------------
# Filtres
# -----------------------------
st.sidebar.header("Filtres")

age_range = st.sidebar.slider(
    "Filtrer par âge",
    int(df.age.min()),
    int(df.age.max()),
    (20, 60)
)

bmi_range = st.sidebar.slider(
    "Filtrer par IMC",
    float(df.bmi.min()),
    float(df.bmi.max()),
    (18.0, 35.0)
)

smoker_filter = st.sidebar.selectbox(
    "Statut fumeur",
    ["Tous", "yes", "no"]
)

# Appliquer filtres
filtered_df = df[
    (df.age >= age_range[0]) &
    (df.age <= age_range[1]) &
    (df.bmi >= bmi_range[0]) &
    (df.bmi <= bmi_range[1])
]

if smoker_filter != "Tous":
    filtered_df = filtered_df[filtered_df.smoker == smoker_filter]

# -----------------------------
# Graphique interactif Plotly
# -----------------------------
fig = px.scatter(
    filtered_df,
    x="age",
    y="bmi",
    size="charges",             # taille proportionnelle aux charges
    color="smoker",             # couleur selon fumeur/non-fumeur
    hover_data=["age","bmi","charges","sex","children","mutuelle_complementaire"],
    labels={"age":"Âge", "bmi":"IMC", "charges":"Frais médicaux (€)", "smoker":"Fumeur"},
    title="Corrélation âge, IMC et frais médicaux"
)

fig.update_traces(marker=dict(opacity=0.7, sizemode='area', sizeref=2.*max(filtered_df.charges)/ (40.**2), line_width=1))
fig.update_layout(legend_title_text='Statut fumeur')

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Infos sur les données filtrées
# -----------------------------
st.write("Nombre d'observations :", len(filtered_df))
