import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox

def render_database_search(uploaded_file):
    if uploaded_file is None:
        return

    # Datei einlesen & Tabellenblatt-Unterstützung für Excel
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        # Excel-Datei laden, um verfügbare Tabellenblätter abzufragen
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        # Tabellenblatt auswählen (falls mehr als eines vorhanden ist)
        if len(sheet_names) > 1:
            selected_sheet = st.selectbox("Tabellenblatt wählen:", sheet_names)
        else:
            selected_sheet = sheet_names[0]

        df = pd.read_excel(excel_file, sheet_name=selected_sheet)

    # 1. Suchspalte wählen
    selected_col = st.selectbox("Suchspalte wählen:", df.columns)

    # 2. Live-Filterung der Optionen beim Tippen
    def search_function(search_term: str):
        if not search_term:
            return []
        values = df[selected_col].dropna().astype(str).unique()
        return [v for v in values if search_term.lower() in v.lower()][:10]

    selected_value = st_searchbox(
        search_function,
        key=f"live_searchbox_{selected_col}",  # Key dynamisch halten für Spaltenwechsel
        placeholder="Tippe zum Suchen..."
    )

    # 3. Ergebnis anzeigen
    if selected_value:
        matches = df[df[selected_col].astype(str) == selected_value]

        if not matches.empty:
            selected_index = matches.index[0]
            if len(matches) > 1:
                options = {idx: f"Zeile {idx + 1}" for idx in matches.index}
                selected_index = st.selectbox("Zeile wählen:", list(options.keys()), format_func=lambda x: options[x])

            selected_row = matches.loc[selected_index]

            for col in df.columns:
                val = selected_row[col]
                
                # Formatierung für Jahreszahlen / Fließkommazahlen
                if isinstance(val, float):
                    if val.is_integer():
                        display_val = str(int(val))
                    else:
                        display_val = f"{val:.2f}".replace('.', ',')
                elif isinstance(val, int):
                    display_val = str(val)
                else:
                    display_val = str(val) if pd.notna(val) else ""

                st.markdown(f"**{col}:**")
                st.code(display_val, language=None)