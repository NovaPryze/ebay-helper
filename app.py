import streamlit as st 
from csvpro import render_database_search

st.title("Verkaufshelfer")

st.divider()

# CSV Upload
col14, col15 = st.columns([1,2], vertical_alignment="center")
with col14:
    st.text("Database vorhanden")

with col15:
    uploaded_file = st.file_uploader(
        "Wähle eine Excel- oder CSV-Datei aus:", 
        type=["csv", "xlsx", "xls"],
        key="user_file_uploader"
        )

# CSV Renderer
render_database_search(uploaded_file)

# Plattform
col12, col13 = st.columns([1,3])
with col12:
    st.text("Plattform wählen")
with col13:
    plattform = st.radio("Plattform auswählen", ["Kleinanzeigen", "ebay"], label_visibility="collapsed")
    max_limit_char = 0
    if plattform == "Kleinanzeigen":
        max_limit_char = 65
    if plattform == "ebay":
        max_limit_char = 80

# Titel
product_title = ""
col9, col11 = st.columns([1,3], vertical_alignment="center")
with col9:
    st.text("Titel eingeben")
with col11:
    product_title = st.text_input("Titel eingeben", placeholder="z. B. Smartphone", max_chars=max_limit_char, label_visibility="collapsed")

# Marke und Modell
col1, col2 = st.columns([1, 3])
with col1: 
    show_marke = st.checkbox("Marke und Modell", value=True)
marke_text = ""
with col2:
    if show_marke:
        marke_text = st.text_input("marke", placeholder="z. B. Samsung Galaxy S25 Ultra", label_visibility="collapsed")

# Bundle
bundle_output = ""
with st.expander("Bundle Items"):
    if "bundle_fields" not in st.session_state:
        st.session_state.bundle_fields = [""]

    if st.button("➕ Weiteres Textfeld hinzufügen"):
        st.session_state.bundle_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.bundle_fields):
        col30, col40 = st.columns([6, 1], vertical_alignment="center")
        
        with col30:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"field_{i}")
            updated_fields.append(val)
            
        with col40:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.bundle_fields.pop(i)
                st.rerun()

    st.session_state.bundle_fields = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.bundle_fields if text]
    bundle_output = "\n".join(formatted_items)

# Grund Verkauf
col3, col4 = st.columns([1, 3])
with col3: 
    show_reason = st.checkbox("Grund für den Verkauf")
reason_text = ""
with col4:
    if show_reason:
        reason_text = st.text_input("reason", placeholder="Grund hier...", label_visibility="collapsed")

# Zustand
col5, col6, col161 = st.columns([1, 1.1, 1.9])
with col5:
    show_zustand = st.checkbox("Zustand", value=True)
zustand_text = ""
with col6:
    if show_zustand:
        zustand_text = st.selectbox("Zustand", ["Sehr gut", "gut", "Defekt"], label_visibility="collapsed")

zustand_zusatz = ""
with col161:
    zustand_zusatz = st.text_input("zusatz", placeholder="Weiteres....", label_visibility="collapsed")

# Lieferumfang
liefer_output = ""
with st.expander("Lieferumfang"):
    if "liefer_fields" not in st.session_state:
        st.session_state.liefer_fields = [""]

    if st.button("➕ Weiteres Item hinzufügen"):
        st.session_state.liefer_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.liefer_fields):
        col10, col20 = st.columns([6, 1], vertical_alignment="center")
        
        with col10:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"item_{i}")
            updated_fields.append(val)
            
        with col20:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete1_{i}"):
                st.session_state.liefer_fields.pop(i)
                st.rerun()

    st.session_state.liefer_fields = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.liefer_fields if text]
    liefer_output = "\n".join(formatted_items)

# Preis
col7, col8 = st.columns([1, 3])
with col7:
    preis_text = st.number_input("preis", placeholder="Preis", label_visibility="collapsed", min_value=0.00, max_value=2000.00, step=0.01, format="%.2f")

with col8:
    preis_art = st.selectbox("preis_art", ["Festpreis","VB","Festpreis zzgl. Versand"], label_visibility="collapsed")

# Technische Daten
daten_output = ""
with st.expander("Technischen Daten"):
    if "daten_fields" not in st.session_state:
        st.session_state.daten_fields = [""]

    if st.button("➕ Weitere Daten hinzufügen"):
        st.session_state.daten_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.daten_fields):
        col50, col60 = st.columns([6, 1], vertical_alignment="center")
        
        with col50:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"data_{i}")
            updated_fields.append(val)
            
        with col60:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete2_{i}"):
                st.session_state.daten_fields.pop(i)
                st.rerun()

    st.session_state.daten_fields = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.daten_fields if text]
    daten_output = "\n".join(formatted_items)

# Besonderheiten
special_output = ""
with st.expander("Besonderheiten"):
    if "special_output" not in st.session_state:
        st.session_state.special_output = [""]

    if st.button("➕ Weitere Besonderheiten hinzufügen"):
        st.session_state.special_output.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.special_output):
        col70, col80 = st.columns([6, 1], vertical_alignment="center")
        
        with col70:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"lol_{i}")
            updated_fields.append(val)
            
        with col80:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete3_{i}"):
                st.session_state.special_output.pop(i)
                st.rerun()

    st.session_state.special_output = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.special_output if text]
    special_output = "\n".join(formatted_items)

# Abholung/Versand
versand = st.selectbox("Versand", ["Abholung", "Versand möglich"])

# Hinweis
hinweis = "Wichtiger Hinweis (Privatverkauf):\nDies ist ein Privatverkauf, daher keine Garantie, Rücknahme oder Gewährleistung. Der Artikel wird unter Ausschluss jeglicher Sachmängelhaftung verkauft."

# Output 

# Basic
if not product_title:
    product_title = "Crazy Product"
preis = f"{preis_text:.2f}{"€"}".replace(".", ",")
basic_output = f"{product_title}{" - "}{zustand_text}{" - "}{preis}\n\n"

# Order: Marke -> Bundle -> Zustand -> Lieferumfang -> T/D -> Grund -> Preis -> V/A -> Hinweis
complex_output = ""

if marke_text:
    complex_output += f"{"Marke und Modell: "}\n{marke_text}\n\n"

if bundle_output:
    complex_output += f"{"Im Bundle enthalten: "}\n{bundle_output}\n\n"

# Zustand
if zustand_zusatz:
    zustand_text += f"{", "}{zustand_zusatz}"
complex_output += f"{"Zustand: "}\n{zustand_text}\n\n"

if liefer_output:
    complex_output += f"{"Liferumfang: "}\n{liefer_output}\n\n"

if daten_output:
    complex_output += f"{"Technische Daten: "}\n{daten_output}\n\n"

if special_output:
    complex_output += f"{"Besonderheiten: "}\n{special_output}\n\n"

if reason_text:
    complex_output += f"{"Grund für Verkauf: "}\n{reason_text}\n\n"

# Preis
complex_output += f"{"Preis: "}\n".replace(".", ",")
complex_output += f"{preis_text:.2f}{"€ "}{preis_art}\n\n"

# Versand
complex_output += f"{"Versand/Abholung: "}\n"
versand_text = f"{"Nur Abholung möglich"}"
if versand == "Versand möglich":
    versand_text = f"{"Gerne Abholung oder gegen Aufpreis Versand möglich"}"  
complex_output += f"{versand_text}\n\n"

output = f"{basic_output}{complex_output}{hinweis}"

st.divider()

st.code(output, language=None)

if st.button("🔄 Reset", type="secondary"):
    # Hier kann noch mehr passieren
    # print("erledigt")    
    st.iframe(
            "<script>window.parent.location.reload();</script>", 
            height=1
        )

st.divider()

st.text("Version: 1.0")