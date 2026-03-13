import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="Vunérabilité Bounkani", layout="wide")

st.title("📊 Évaluation des Besoins : Région du Bounkani")
st.info("Formulaire de collecte terrain (Mode Local Sécurisé)")

with st.form("enquete_form", clear_on_submit=True):
    # SECTION 1: ADMINISTRATION
    st.header("1. Administration & Collecte")
    col1, col2 = st.columns(2)
    with col1:
        chef_equipe = st.text_input("Nom du chef d'équipe")
        enqueteur = st.text_input("Nom de l'enquêteur")
    with col2:
        contact_chef = st.text_input("Contact du chef d'équipe")
        date_coll = st.date_input("Date de collecte", date.today())

    # SECTION 2: LOCALISATION
    st.header("2. Localisation")
    c1, c2, c3 = st.columns(3)
    with c1:
        region = st.text_input("Région", value="Bounkani", disabled=True)
    with c2:
        departement = st.selectbox("Département", ["Bouna", "Nassian", "Doropo", "Tehini"])
    with c3:
        sp_commune = st.text_input("Sous-Préfecture / Commune / Village")

    # SECTION 3: IDENTIFICATION
    st.header("3. Identification de l'enquêté")
    col_id1, col_id2, col_id3 = st.columns(3)
    with col_id1:
        qualite_enquete = st.selectbox("L'enquêté est :", ["Chef de ménage", "Autre membre de la famille"])
        nom_chef = st.text_input("Nom et prénoms du Chef de ménage")
    with col_id2:
        sexe_chef = st.radio("Sexe du Chef de ménage", ["Masculin", "Féminin"])
        age_chef = st.number_input("Âge du Chef de ménage", min_value=0, max_value=120)
    with col_id3:
        nationalite = st.selectbox("Nationalité", ["Ivoirienne", "Autre"])
        contact_enquete = st.text_input("Contact téléphonique")

    st.divider()

    # SECTION 4-5-6 : WASH & ALIM
    st.header("4. Secteurs WASH & Alimentation")
    w1, w2, w3 = st.columns(3)
    with w1:
        traitement_eau = st.selectbox("Traitement de l'eau", ["Rien", "Ébullition", "Chlore", "Filtre"])
    with w2:
        repas_adultes = st.number_input("Repas/jour (Adultes)", 0, 4, 1)
    with w3:
        structure_mur = st.selectbox("Type de murs", ["Banco", "Dur", "Paille"])
    
    scolarisation = st.selectbox("Scolarisation des enfants", ["Tous", "Certains", "Aucun"])

    submit = st.form_submit_button("ENREGISTRER LA FICHE")

# --- TRAITEMENT DES DONNÉES ---
file_path = "donnees_bounkani.csv"

if submit:
    # Création du dictionnaire de données
    data = {
        "Date": [str(date_coll)],
        "Chef_Equipe": [chef_equipe],
        "Enqueteur": [enqueteur],
        "Departement": [departement],
        "Localite": [sp_commune],
        "Chef_Menage": [nom_chef],
        "Sexe": [sexe_chef],
        "Nationalite": [nationalite],
        "WASH_Traitement": [traitement_eau],
        "Alim_Repas_Adult": [repas_adultes],
        "Abris_Mur": [structure_mur],
        "Scolarisation": [scolarisation]
    }
    df_new = pd.DataFrame(data)

    # Sauvegarde CSV (Mode Ajout)
    if not os.path.isfile(file_path):
        df_new.to_csv(file_path, index=False, encoding='utf-8')
    else:
        df_new.to_csv(file_path, mode='a', index=False, header=False, encoding='utf-8')

    st.success(f"✅ Fiche de {nom_chef} enregistrée avec succès sur le serveur !")
    st.balloons()

# --- ESPACE ADMINISTRATEUR (Pour vous) ---
st.sidebar.divider()
st.sidebar.header("Zone Administrateur")
if os.path.isfile(file_path):
    df_collecte = pd.read_csv(file_path)
    st.sidebar.write(f"Nombre de fiches collectées : **{len(df_collecte)}**")
    
    with open(file_path, "rb") as f:
        st.sidebar.download_button(
            label="📥 Télécharger la base de données (CSV)",
            data=f,
            file_name=f"collecte_bounkani_{date.today()}.csv",
            mime="text/csv"
        )
else:
    st.sidebar.info("Aucune donnée collectée pour le moment.")
