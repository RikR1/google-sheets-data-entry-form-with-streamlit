import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import pygwalker as pyg

st.set_page_config(
    page_title="RR",
    page_icon=":lion:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Display Title and Description
st.title("Plotting Finance")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# existing data entrate
existing_data_entrate = conn.read(worksheet="Entrate", usecols=list(range(13)), ttl=5)
existing_data_entrate = existing_data_entrate.dropna(how="all")
existing_data_entrate = existing_data_entrate.drop(existing_data_entrate.index[-1])

# Dividere la colonna 'Date' in giorno, mese e anno
existing_data_entrate[['Giorno', 'Mese', 'Anno']] = existing_data_entrate['Data'].str.split('/', expand=True)

existing_data_entrate = existing_data_entrate.drop(columns=["Data"])

#existing_data_entrate[['Giorno', 'Mese', 'Anno']] = existing_data_entrate[['Giorno', 'Mese', 'Anno']].astype()

#existing_data_entrate["Data"] = pd.to_datetime(existing_data_entrate["Data"],dayfirst=True)




pyg.walk(existing_data_entrate, env='Streamlit', dark='dark')
