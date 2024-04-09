import streamlit as st
import pickle
import pandas as pd
from supabase import create_client, Client
import os
from utils import *

from dotenv import load_dotenv
load_dotenv()


st.markdown(f"<p style='text-align: center;'>{img_to_html('data/M1.png')}</p>", unsafe_allow_html=True)
base = 'dark'
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

with open("model.pkl", "rb") as file:
    model = pickle.load(file)




col1, col2 = st.columns(2)

with col1:
    st.title('')
    data = {
        "Code postal" : st.number_input("Code postal", value=None),
        "Surface Carrez du 1er lot" : st.number_input("Surface Carrez"),
        "Nombre pieces principales" : st.number_input("Nombre pieces principales"),
    }

    data = pd.DataFrame(data, index=["1"])
    pred = model.predict(data.values[:1])[0]
    m2 = data["Surface Carrez du 1er lot"].astype(float).values




with col2:

    col1, col2 = st.columns(2)
    with col1:
        pass
    with col2:
        st.title(f"{round(pred)}€")
        st.title("")
        if (pred / m2 > 2800) and (pred / m2 < 3400):
            st.image("data/orange gauge.png")

        elif pred/m2  > 4000:
            st.image("data/red gauge.png")

        else:
            st.image("data/green gauge.png")

data = supabase.table('prediction').insert({"Code postal":"Code postal",
                                            "Surface Carrez du 1er lot": "Surface Carrez du 1er lot",
                                            "Nombre pieces principales":"Nombre pieces principales",
                                            "Pred":pred}).execute()
