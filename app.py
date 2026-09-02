import streamlit as st 
import pandas as pd 

st.title("Ebay Helper")

product_title = st.text_input("Titel eingeben", placeholder="z. B. Smartphone")

col1, col2 = st.columns([1, 3])
with col1: 
    show_feature = st.checkbox("Feature")
feature_text = ""
with col2:
    if show_feature:
        feature_text = st.text_input("Eingabe", placeholder="Feature hier...", label_visibility="collapsed")


col3, col4 = st.columns([1, 3])
with col3: 
    show_feature2 = st.checkbox("Feature 2")
feature_text2 = ""
with col4:
    if show_feature2:
        feature_text2 = st.text_input("Eingabe2", placeholder="Feature hier...", label_visibility="collapsed")

output = f"{product_title}\n\n{feature_text}\n{feature_text2}"

st.divider()

st.code(output, language=None)