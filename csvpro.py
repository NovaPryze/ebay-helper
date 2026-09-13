import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox

def render_database_search(uploaded_file):
    if uploaded_file is None:
        return

    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    selected_col = st.selectbox("Suchspalte wählen:", df.columns)

    # Funktion zur Live-Filterung der Optionen beim Tippen
    def search_function(search_term: str):
        if not search_term:
            return []
        values = df[selected_col].dropna().astype(str).unique()
        return [v for v in values if search_term.lower() in v.lower()][:10]

    selected_value = st_searchbox(
        search_function,
        key="live_searchbox",
        placeholder="Tippe zum Suchen..."
    )

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