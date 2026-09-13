import streamlit as st 
from csvpro import render_database_search

# StartCommand: python -m streamlit run app.py

st.title("Verkaufshelfer")

st.divider()

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Einstellungen")
    
    show_db = st.toggle(
        "🔍 CSV / Excel Suche aktivieren", 
        value=st.session_state.get("show_db_search", True),
        key="show_db_search"
    )

    show_useless = st.toggle(
        "⚙️ Hier passiert noch gar nix", 
        value=st.session_state.get("show_useless_key", False),
        key="show_useless_key"
    )

    if show_db:
        st.subheader("📁 Datei Auswählen")
        
        uploaded_file = st.file_uploader(
            "Datei auswählen:", 
            type=["csv", "xlsx", "xls"],
            key="user_file_uploader",
            label_visibility='collapsed'
        )
        
        # Aufruf der minimalistischen Suche
        render_database_search(uploaded_file)

    if show_useless:
        st.error("Ur stupid")


# ---Mainpage---

# 0. Reset-Counter für sauberes Zurücksetzen initialisieren
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# Plattform
col12, col13 = st.columns([1,3])
with col12:
    st.text("Plattform wählen")
with col13:
    plattform = st.radio("Plattform auswählen", ["Kleinanzeigen", "ebay"], label_visibility="collapsed", key=f"plattform_{st.session_state.reset_counter}")
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
    product_title = st.text_input("Titel eingeben", placeholder="z. B. Smartphone", max_chars=max_limit_char, label_visibility="collapsed", key=f"product_title_{st.session_state.reset_counter}")

# Marke und Modell
col1, col2 = st.columns([1, 3])
with col1: 
    show_marke = st.checkbox("Marke und Modell", value=True, key=f"show_marke_{st.session_state.reset_counter}")
marke_text = ""
with col2:
    if show_marke:
        marke_text = st.text_input("marke", placeholder="z. B. Samsung Galaxy S25 Ultra", label_visibility="collapsed", key=f"marke_text_{st.session_state.reset_counter}")

# Bundle
bundle_output = ""
with st.expander("Bundle Items"):
    if "bundle_fields" not in st.session_state:
        st.session_state.bundle_fields = [""]

    if st.button("➕ Weiteres Textfeld hinzufügen", key=f"btn_bundle_{st.session_state.reset_counter}"):
        st.session_state.bundle_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.bundle_fields):
        col30, col40 = st.columns([6, 1], vertical_alignment="center")
        
        with col30:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"field_{i}_{st.session_state.reset_counter}")
            updated_fields.append(val)
            
        with col40:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete_{i}_{st.session_state.reset_counter}"):
                st.session_state.bundle_fields.pop(i)
                st.rerun()

    st.session_state.bundle_fields = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.bundle_fields if text]
    bundle_output = "\n".join(formatted_items)

# Grund Verkauf
col3, col4 = st.columns([1, 3])
with col3: 
    show_reason = st.checkbox("Grund für den Verkauf", key=f"show_reason_{st.session_state.reset_counter}")
reason_text = ""
with col4:
    if show_reason:
        reason_text = st.text_input("reason", placeholder="Grund hier...", label_visibility="collapsed", key=f"reason_text_{st.session_state.reset_counter}")

# Zustand
col5, col6, col161 = st.columns([1, 1.1, 1.9])
with col5:
    show_zustand = st.checkbox("Zustand", value=True, key=f"show_zustand_{st.session_state.reset_counter}")
zustand_text = ""
with col6:
    if show_zustand:
        zustand_text = st.selectbox("Zustand", ["Sehr gut", "gut", "Defekt"], label_visibility="collapsed", key=f"zustand_select_{st.session_state.reset_counter}")

zustand_zusatz = ""
with col161:
    zustand_zusatz = st.text_input("zusatz", placeholder="Weiteres....", label_visibility="collapsed", key=f"zustand_zusatz_{st.session_state.reset_counter}")

# Lieferumfang
liefer_output = ""
with st.expander("Lieferumfang"):
    if "liefer_fields" not in st.session_state:
        st.session_state.liefer_fields = [""]

    if st.button("➕ Weiteres Item hinzufügen", key=f"btn_liefer_{st.session_state.reset_counter}"):
        st.session_state.liefer_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.liefer_fields):
        col10, col20 = st.columns([6, 1], vertical_alignment="center")
        
        with col10:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"item_{i}_{st.session_state.reset_counter}")
            updated_fields.append(val)
            
        with col20:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete1_{i}_{st.session_state.reset_counter}"):
                st.session_state.liefer_fields.pop(i)
                st.rerun()

    st.session_state.liefer_fields = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.liefer_fields if text]
    liefer_output = "\n".join(formatted_items)

# Preis
col7, col8 = st.columns([1, 3])
with col7:
    preis_text = st.number_input("preis", placeholder="Preis", label_visibility="collapsed", min_value=0.00, max_value=2000.00, step=0.01, format="%.2f", key=f"preis_text_{st.session_state.reset_counter}")

with col8:
    preis_art = st.selectbox("preis_art", ["Festpreis","VB","Festpreis zzgl. Versand"], label_visibility="collapsed", key=f"preis_art_{st.session_state.reset_counter}")

# Technische Daten
daten_output = ""
with st.expander("Technischen Daten"):
    if "daten_fields" not in st.session_state:
        st.session_state.daten_fields = [""]

    if st.button("➕ Weitere Daten hinzufügen", key=f"btn_daten_{st.session_state.reset_counter}"):
        st.session_state.daten_fields.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.daten_fields):
        col50, col60 = st.columns([6, 1], vertical_alignment="center")
        
        with col50:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"data_{i}_{st.session_state.reset_counter}")
            updated_fields.append(val)
            
        with col60:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete2_{i}_{st.session_state.reset_counter}"):
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

    if st.button("➕ Weitere Besonderheiten hinzufügen", key=f"btn_special_{st.session_state.reset_counter}"):
        st.session_state.special_output.append("")
        st.rerun()

    updated_fields = []
    for i, content in enumerate(st.session_state.special_output):
        col70, col80 = st.columns([6, 1], vertical_alignment="center")
        
        with col70:
            val = st.text_input(f"Item {i + 1}", value=content, key=f"lol_{i}_{st.session_state.reset_counter}")
            updated_fields.append(val)
            
        with col80:
            st.write("") 
            st.write("")
            if st.button("🗑️", key=f"delete3_{i}_{st.session_state.reset_counter}"):
                st.session_state.special_output.pop(i)
                st.rerun()

    st.session_state.special_output = updated_fields
    formatted_items = [f"- {text}" for text in st.session_state.special_output if text]
    special_output = "\n".join(formatted_items)

# Abholung/Versand
versand = st.selectbox("Versand", ["Abholung", "Versand möglich"], key=f"versand_{st.session_state.reset_counter}")

# Hinweis
hinweis = "Wichtiger Hinweis (Privatverkauf):\nDies ist ein Privatverkauf, daher keine Garantie, Rücknahme oder Gewährleistung. Der Artikel wird unter Ausschluss jeglicher Sachmängelhaftung verkauft."

# Output 

# Basic
if not product_title:
    product_title = "Crazy Product"
preis = f"{preis_text:.2f}{'€'}".replace(".", ",")
basic_output = f"{product_title}{' - '}{zustand_text}{' - '}{preis}\n\n"

# Order: Marke -> Bundle -> Zustand -> Lieferumfang -> T/D -> Grund -> Preis -> V/A -> Hinweis
complex_output = ""

if marke_text:
    complex_output += f"{'Marke und Modell: '}\n{marke_text}\n\n"

if bundle_output:
    complex_output += f"{'Im Bundle enthalten: '}\n{bundle_output}\n\n"

# Zustand
if zustand_zusatz:
    zustand_text += f"{', '}{zustand_zusatz}"
complex_output += f"{'Zustand: '}\n{zustand_text}\n\n"

if liefer_output:
    complex_output += f"{'Liferumfang: '}\n{liefer_output}\n\n"

if daten_output:
    complex_output += f"{'Technische Daten: '}\n{daten_output}\n\n"

if special_output:
    complex_output += f"{'Besonderheiten: '}\n{special_output}\n\n"

if reason_text:
    complex_output += f"{'Grund für Verkauf: '}\n{reason_text}\n\n"

# Preis
complex_output += f"{'Preis: '}\n".replace(".", ",")
complex_output += f"{preis_text:.2f}{'€ '}{preis_art}\n\n"

# Versand
complex_output += f"{'Versand/Abholung: '}\n"
versand_text = f"{'Nur Abholung möglich'}"
if versand == "Versand möglich":
    versand_text = f"{'Gerne Abholung oder gegen Aufpreis Versand möglich'}"  
complex_output += f"{versand_text}\n\n"

output = f"{basic_output}{complex_output}{hinweis}"

st.divider()

st.code(output, language=None)

if st.button("🔄 Reset", type="secondary", key=f"reset_btn_{st.session_state.reset_counter}"):
    # 1. Dynamische Listen leeren
    st.session_state.bundle_fields = [""]
    st.session_state.liefer_fields = [""]
    st.session_state.daten_fields = [""]
    st.session_state.special_output = [""]
    
    # 2. Counter erhöhen (zwingt alle Widgets zur Neuinitialisierung)
    st.session_state.reset_counter += 1
    
    # 3. Reines Streamlit-Rerun anstelle eines Browser-F5-Reloads
    st.rerun()

st.divider()

st.text("Version: 2.2")