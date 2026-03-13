import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Vunérabilité Bounkani", layout="wide")

st.title("📊 Évaluation des Besoins : Région du Bounkani")
st.info("Les données saisies sont transmises directement au QG via Google Sheets.")

# --- CONNEXION GOOGLE SHEETS ---
# Note : Vous devrez configurer l'URL dans vos secrets Streamlit plus tard
# --- CONNEXION GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("enquete_form"):
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

    # SECTION 3: IDENTIFICATION DE L'ENQUÊTÉ (Source PDF)
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

    # SECTION 4-5-6 : WASH, ALIM, ABRIS (Source Excel)
    st.header("4. Secteurs WASH, Alimentation & Abris")
    w1, w2, w3 = st.columns(3)
    with w1:
        traitement_eau = st.selectbox("Traitement de l'eau", ["Rien", "Ébullition", "Chlore", "Filtre"])
    with w2:
        repas_adultes = st.number_input("Repas/jour (Adultes)", 0, 4, 1)
    with w3:
        structure_mur = st.selectbox("Type de murs", ["Banco", "Dur", "Paille"])
    
    scolarisation = st.selectbox("Scolarisation des enfants", ["Tous", "Certains", "Aucun"])

    # Validation
    submit = st.form_submit_button("ENREGISTRER ET ENVOYER AU QG")

if submit:
    try:
        # 1. Création de la nouvelle ligne avec les bons noms de colonnes
        new_row = {
            "Date": str(date_coll),
            "Enqueteur": enqueteur,
            "Localite": sp_commune,
            "Chef_Menage": nom_chef,
            "Sexe": sexe_chef,
            "Nationalite": nationalite,
            "WASH_Traitement": traitement_eau,
            "Alim_Repas_Adultes": repas_adultes,
            "Abris_Mur": structure_mur,
            "Scolarisation": scolarisation
        }
        
        # 2. Lecture et mise à jour simplifiée
        existing_data = conn.read() # Il va lire l'URL directement dans vos secrets
        updated_df = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
        
        conn.update(data=updated_df) # Il va écrire via vos secrets
        
        st.success("✅ Données envoyées avec succès au QG !")
        st.balloons()
    except Exception as e:
        st.error(f"Détail de l'erreur : {e}")
