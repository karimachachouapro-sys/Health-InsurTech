# streamlit_app.py

import streamlit as st

# ---------------------------
# 0️⃣ Initialisation session
# ---------------------------
if "cookies_accepted" not in st.session_state:
    st.session_state.cookies_accepted = False

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ---------------------------
# 1️⃣ Consentement RGPD
# ---------------------------
if not st.session_state.cookies_accepted:

    st.title("🍪 Consentement RGPD")

    st.write("""
    Cette application utilise uniquement des cookies techniques nécessaires
    au bon fonctionnement de l'application.

    Les informations saisies dans les formulaires ne sont pas stockées et
    servent uniquement à effectuer des estimations de frais médicaux.
    """)

    if st.button("J'accepte les cookies"):
        st.session_state.cookies_accepted = True
        st.rerun()


# ---------------------------
# 2️⃣ Authentification
# ---------------------------
elif not st.session_state.authenticated:

    st.title("🔐 Connexion à l'application")

    st.write("Veuillez vous connecter pour accéder aux fonctionnalités.")

    USERNAME = "admin"
    PASSWORD = "admin"

    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):

        if username_input == USERNAME and password_input == PASSWORD:

            st.session_state.authenticated = True
            st.success("Connexion réussie")
            st.rerun()

        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")


# ---------------------------
# 3️⃣ Page d'accueil
# ---------------------------
else:

    st.title("🏥 Health-InsurTech")

    st.subheader("Présentation du projet")

    st.write("""
    **Health-InsurTech** est une application de data science permettant
    d'explorer un dataset de frais médicaux et d'estimer les charges
    annuelles d'un individu à partir de plusieurs caractéristiques.

    L'objectif est de démontrer l'utilisation de techniques de **machine learning**
    dans le domaine de l'assurance santé tout en proposant une interface
    interactive accessible aux utilisateurs.
    """)

    st.subheader("Fonctionnalités de l'application")

    st.write("""
    L'application est organisée en trois pages principales :
    """)

    st.markdown("""
    **📊 Data**

    - Statistiques descriptives
    - Dashboard interactif montrant la corrélation entre :
      - l'âge
      - l'IMC
      - les frais médicaux

    **🤖 Modèle**

    - Entraînement d'un modèle de **régression linéaire**
    - Analyse des performances du modèle (RMSE, R²)
    - Visualisation des coefficients
    - Analyse de l'impact des variables sur les prédictions

    **🧮 Simulation**

    - Formulaire interactif permettant de saisir :
      - âge
      - IMC
      - statut fumeur
      - nombre d'enfants
      - mutuelle
    - Estimation des frais médicaux annuels à l'aide du modèle entraîné
    """)

    st.info("Utilisez le menu latéral pour naviguer entre les différentes pages.")
