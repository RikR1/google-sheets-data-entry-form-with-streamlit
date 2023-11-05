import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import pygwalker as pyg


# Display Title and Description
st.title("Entry Form RR Personal Finance")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# existing data entrate
existing_data_entrate = conn.read(worksheet="Entrate", usecols=list(range(13)), ttl=5)
existing_data_entrate = existing_data_entrate.dropna(how="all")

# existing data uscite
existing_data_uscite = conn.read(worksheet="Uscite", usecols=list(range(5)), ttl=5)
existing_data_uscite = existing_data_uscite.dropna(how="all")

action = st.selectbox(
    "Scegli un'opzione",
    [
        "Inserisci un'entrata",
        "Inserisci un'uscita",
        "Visualizza DataSet"
    ]
)

# List Macro Category
MACRO_CATEGORY = [
    "Personale",
    "Investimenti",
    "Auto",
    "Trasporti",
    "Famiglia"
]
if action == "Inserisci un'uscita":

    macro_category = st.selectbox("Macro Categoria Spese*", options=MACRO_CATEGORY, index=None)

    if macro_category == "Personale":
            CATEGORY = [
                "Spese varie personali",
                "Casa",
                "Svago",
                "Vacanze",
                "Debiti"
            ]
    elif macro_category == "Investimenti":
        CATEGORY = [
            "Fondo investimenti",
            "Formazione",
            "Risparmi",
        ]
    elif macro_category == "Auto":
        CATEGORY = [
            "Rata prestito",
            "Assicurazione",
            "Bollo",
            "Manutenzion ordinaria",
            "Manutenzion straordinaria",
        ]
    elif macro_category == "Trasporti":
        CATEGORY = [
            "Carburante",
            "Trasporti pubblici",
            "Voli",
            "Casello",
            "Parcheggi",
        ]
    elif macro_category == "Famiglia":
        CATEGORY = [
            "Spese varie famiglia",
            "Spese casa famiglia",
        ]
    else:
            CATEGORY = []

    category = st.selectbox("Categoria*", options=CATEGORY)

if action == "Inserisci un'entrata":
    st.markdown("Inserisci la nuova Entrata")

    with st.form(key="Entrate"):

        data = st.date_input("Data*", (datetime.date.today()))
        paga_oraria = st.number_input("Paga oraria", value=0.0000, step=0.0001,format="%f")
        ore_lavorative = st.number_input(label="Ore lavorative*", value=0.00, format="%f")
        #lordo = st.write("Lordo: ", paga_oraria*ore_lavorative)
        totale_trattenute = st.number_input(label="Totale trattenute*", value=0.00, format="%f")
        tfr = st.number_input(label="TFR*", value=None, placeholder="Type a number...")
        #netto = st.write("Netto: ", (paga_oraria*ore_lavorative)-totale_trattenute)
        bonus = st.number_input(label="Bonus*", value=None, placeholder="Type a number...")
        fuori_busta = st.number_input(label="Fuori busta*", value=None, placeholder="Type a number...")
        straordinari = st.number_input(label="Straordinari*", value=None, placeholder="Type a number...")
        tredicesima = st.number_input(label="Tredicesima*", value=None, placeholder="Type a number...")
        entrate_secondarie = st.number_input(label="Entrate secondarie*", value=None, placeholder="Type a number...")
        
        # Mark mandatory fields
        st.markdown("**required*")

        submit_button = st.form_submit_button(label="Inserisci")



    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not data or not paga_oraria:
            st.warning("Tutti i campi con l'asterisco sono obbligatori")
            st.stop()

        else:
            # Create a new row of vendor data
            Entrata = pd.DataFrame(
                [
                    {
                        "Data": data.strftime("%y-%m-%d"),
                        "Paga oraria": paga_oraria,
                        "Ore lavorative": ore_lavorative,
                        "Totale trattenute": totale_trattenute,
                        "TFR": tfr,
                        "Bonus": bonus,
                        "Fuori busta": fuori_busta,
                        "Straordinari": straordinari,
                        "Tredicesima": tredicesima,
                        "TFR": tfr,
                        "Entrate secondarie": entrate_secondarie,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            existing_data_entrate = existing_data_entrate.drop(existing_data_entrate.index[-1])
            updated_df_entrate = pd.concat([existing_data_entrate, Entrata], ignore_index=True)

            riga_TOT = updated_df_entrate.iloc[:, 3:].sum()


            updated_df_entrate["Importo lordo"] = '=INDIRECT(CONCAT("B";ROW()))*INDIRECT(CONCAT("C";ROW()))'
            updated_df_entrate["Importo netto"] = '=INDIRECT(CONCAT("D";ROW()))-INDIRECT(CONCAT("E";ROW()))'
            updated_df_entrate["Totale"] = '=INDIRECT(CONCAT("G";ROW()))+INDIRECT(CONCAT("H";ROW()))+INDIRECT(CONCAT("I";ROW()))+INDIRECT(CONCAT("J";ROW()))+INDIRECT(CONCAT("K";ROW()))+INDIRECT(CONCAT("L";ROW()))'

            updated_df_entrate = updated_df_entrate.append(riga_TOT,ignore_index= True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Entrate", data=updated_df_entrate)

            st.success("Entrata inserita con successo!")


elif action == "Inserisci un'uscita":
    
    
    st.markdown("Inserisci la nuova Uscita")

    with st.form(key="Uscite"):
        data_uscite = st.date_input("Data*", (datetime.date.today()))
        st.text(macro_category) #"Macro Categoria: ", 
        st.text(category) #"Categoria: ", 
        descrizione = st.text_input(label="Descrizione")
        importo = st.number_input(label="Importo*", value=0.00, format="%f")

        # Mark mandatory fields
        st.markdown("**required*")

        submit_button_uscite = st.form_submit_button(label="Inserisci")

    if submit_button_uscite:
        # Check if all mandatory fields are filled
        if not data_uscite or not importo:
            st.warning("Tutti i campi con l'asterisco sono obbligatori")
            st.stop()

        else:
            # Create a new row of vendor data
            Uscita = pd.DataFrame( 
                [
                    {
                        "Data": data_uscite.strftime("%y-%m-%d"),
                        "Macro Categoria": macro_category,
                        "Categoria": category,
                        "Descrizione": descrizione,
                        "Importo": importo,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            existing_data_uscite = existing_data_uscite.drop(existing_data_uscite.index[-1])
            updated_df_uscite = pd.concat([existing_data_uscite, Uscita], ignore_index=True)

            riga_TOT_uscite = updated_df_uscite.iloc[:, 4:].sum()

            updated_df_uscite = updated_df_uscite.append(riga_TOT_uscite,ignore_index= True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Uscite", data=updated_df_uscite)

            st.success("Entrata inserita con successo!")

 

elif action == "Visualizza DataSet":

    DATASET = ["DataSet entrate","DataSet uscite"]
    
    data_select = st.selectbox("Dataset", options=DATASET, index=None)

    if data_select == "DataSet entrate":
        st.dataframe(existing_data_entrate)
    elif data_select == "DataSet uscite":
        st.dataframe(existing_data_uscite)
    else:
        st.markdown("Seleziona un'opzione")