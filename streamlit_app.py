import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime


# Display Title and Description
st.title("Entrate")
st.markdown("Inserisci i dati nei campi sottostanti")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Entrate", usecols=list(range(13)))#, ttl=5)
existing_data = existing_data.dropna(how="all")

#st.dataframe(existing_data)

#

# List of Business Types and Products
#BUSINESS_TYPES = [
#    "Manufacturer",
#    "Distributor",
#    "..."
#]
   #business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    

#PRODUCTS = [
#    "Electronics",
#    "Apparel",
#    "..."
#]
    #products = st.multiselect("Products Offered", options=PRODUCTS)

# Onboarding New Vendor Form
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
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
#        elif existing_data["Data"].str.contains(data).any():
#            st.warning("Questo mese è già inserito")
#            st.stop()
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
            existing_data = existing_data.drop(existing_data.index[-1])
            updated_df = pd.concat([existing_data, Entrata], ignore_index=True)

            riga_TOT = updated_df.iloc[:, 3:].sum()


            updated_df["Importo lordo"] = '=INDIRECT(CONCAT("B";ROW()))*INDIRECT(CONCAT("C";ROW()))'
            updated_df["Importo netto"] = '=INDIRECT(CONCAT("D";ROW()))-INDIRECT(CONCAT("E";ROW()))'
            updated_df["Totale"] = '=INDIRECT(CONCAT("G";ROW()))+INDIRECT(CONCAT("H";ROW()))+INDIRECT(CONCAT("I";ROW()))+INDIRECT(CONCAT("J";ROW()))+INDIRECT(CONCAT("K";ROW()))+INDIRECT(CONCAT("L";ROW()))'

            updated_df = updated_df.append(riga_TOT,ignore_index= True)


            


            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Entrate", data=updated_df)

            st.success("Entrata inserita con successo!") 