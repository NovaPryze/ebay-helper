import streamlit as st
import pandas as pd

@st.cache_data
def load_data(uploaded_file) -> pd.DataFrame:
    """Liest eine hochgeladene CSV- oder Excel-Datei ein."""
    try:
        # Prüfen der Dateiendung anhand des ursprünglichen Dateinamens
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Fehler beim Lesen der Datei: {e}")
        return pd.DataFrame()

def render_database_search(uploaded_file, search_column: str = None):
    """Rendert die Suchmaske und Detailansicht für die ausgewählte Datei."""
    if uploaded_file is None:
        st.info("👆 Bitte wähle zuerst eine Datei von deinem Rechner aus.")
        return

    # Daten laden
    df = load_data(uploaded_file)
    
    if df.empty:
        st.warning("Die Datei ist leer oder konnte nicht verarbeitet werden.")
        return

    st.success(f"Datei **'{uploaded_file.name}'** erfolgreich geladen ({len(df)} Zeilen).")
    st.subheader("🔍 Suche in den Daten")

    # Auswahl der Suchspalte
    columns = list(df.columns)
    selected_col = search_column if search_column in columns else st.selectbox(
        "Suchspalte wählen:", 
        options=columns,
        key="search_col_select"
    )

    # Suchfeld
    search_term = st.text_input(
        "Suchbegriff eingeben...", 
        key="db_search_input"
    )

    # Suche ausführen
    if search_term.strip():
        matches = df[df[selected_col].astype(str).str.contains(search_term, case=False, na=False)]

        if matches.empty:
            st.info("Keine passenden Einträge gefunden.")
        else:
            st.success(f"{len(matches)} Treffer gefunden:")

            # Bei mehreren Treffern Zeile auswählen
            selected_index = matches.index[0]
            if len(matches) > 1:
                options = {idx: f"{row[selected_col]} (Zeile {idx + 1})" for idx, row in matches.iterrows()}
                selected_index = st.selectbox(
                    "Passenden Eintrag auswählen:", 
                    options=list(options.keys()), 
                    format_func=lambda x: options[x],
                    key="select_matched_entry"
                )

            selected_row = matches.loc[selected_index]

            st.write("---")
            st.markdown("### Detailansicht Spalten")

            # Ausgabe jeder Spalte in einem eigenen Code-Block
            for col in columns:
                val = selected_row[col]
                display_val = str(val) if pd.notna(val) else ""
                
                st.markdown(f"**{col}:**")
                st.code(display_val, language=None)