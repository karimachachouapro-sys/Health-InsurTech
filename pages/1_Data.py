import streamlit as st
import pandas as pd
import os
import altair as alt

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
- **l'âge**
- **l'IMC**
- **les frais médicaux**
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
# Graphique interactif
# -----------------------------
chart = alt.Chart(filtered_df).mark_circle(size=80, opacity=0.7).encode(
    x=alt.X("age", title="Âge"),
    y=alt.Y("bmi", title="IMC"),
    color=alt.Color(
        "charges",
        title="Frais médicaux (€)",
        scale=alt.Scale(scheme="redyellowblue")
    ),
    tooltip=[
        alt.Tooltip("age", title="Âge"),
        alt.Tooltip("bmi", title="IMC"),
        alt.Tooltip("charges", title="Charges (€)"),
        alt.Tooltip("smoker", title="Fumeur")
    ]
).interactive()

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# Infos sur les données filtrées
# -----------------------------
st.write("Nombre d'observations :", len(filtered_df))