
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from matplotlib import pyplot as plt
import plotly.express as px

st.set_page_config(page_title="AI Maturity Dashboard", layout="wide")

st.sidebar.title("AI Maturity Dashboard")
page = st.sidebar.selectbox("Seite wählen", ["Assessment", "Ergebnisse", "Export", "Strategie-Agent"])

if page == "Assessment":
    st.title("Maturity Assessment")
    st.write("Bitte beantworten Sie die folgenden Fragen, um den Maturity-Level Ihres Unternehmens zu ermitteln.")

    questions = {
        "Governance-Strukturen vorhanden": None,
        "Dokumentation der KI-Systeme": None,
        "Bias-Mitigation umgesetzt": None,
        "Datenstrategie vorhanden": None,
        "Transparenz der Modelle sichergestellt": None,
        "Risikobewertung regelmäßig durchgeführt": None,
    }

    scores = {}
    for q in questions:
        scores[q] = st.slider(q, 1, 5, 3)

    if st.button("Analyse starten"):
        df = pd.DataFrame([scores])
        st.session_state["score_df"] = df
        st.success("Analyse abgeschlossen – bitte wechseln Sie zu 'Ergebnisse'.")

elif page == "Ergebnisse":
    st.title("Ergebnisse & Bewertung")

    if "score_df" not in st.session_state:
        st.warning("Bitte zuerst das Assessment ausfüllen.")
    else:
        df = st.session_state["score_df"]
        st.subheader("Radar-Chart")
        fig = px.line_polar(
            r=df.iloc[0].values,
            theta=list(df.columns),
            line_close=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Handlungsempfehlung")
        avg_score = df.mean(axis=1).iloc[0]
        if avg_score >= 4:
            st.success("Ihr KI-System zeigt einen hohen Reifegrad. Fokus: Optimierung & Skalierung.")
        elif avg_score >= 2.5:
            st.info("Solider Zwischenstand. Empfohlen: Governance & Transparenz stärken.")
        else:
            st.error("Niedriger Reifegrad. Empfehlung: Grundlegende Strukturen & Prozesse aufbauen.")

elif page == "Export":
    st.title("Export & Report")
    if "score_df" in st.session_state:
        df = st.session_state["score_df"]
        st.download_button("Download CSV", df.to_csv(index=False), file_name="assessment_results.csv")

        st.markdown("### Beispielhafter Report")
        st.write("Dies ist ein Mockup eines OnePagers, den Sie Ihrem Unternehmen vorlegen könnten.")
        st.image("https://via.placeholder.com/800x400?text=AI+Assessment+Report", caption="Report-Vorschau")

    else:
        st.warning("Noch keine Ergebnisse zum Export vorhanden.")

elif page == "Strategie-Agent":
    st.title("GPT-gestützter Strategie-Agent")
    user_input = st.text_area("Stellen Sie eine Frage zur KI-Strategie, z. B. 'Wie starte ich eine Governance-Struktur?'")
    if st.button("Antwort generieren"):
        st.info("Dies ist ein Platzhalter für GPT-Antworten – Integration folgt im nächsten Schritt.")
