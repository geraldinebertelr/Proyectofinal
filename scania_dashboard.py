from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


CURRENT_FILE = Path(__file__).resolve()
CANDIDATE_TABLE_DIRS = [
    CURRENT_FILE.parent / "reports" / "scania_project" / "tables",
    CURRENT_FILE.parent.parent / "reports" / "scania_project" / "tables",
    CURRENT_FILE.parent / "tables",
    CURRENT_FILE.parent.parent / "tables",
    CURRENT_FILE.parent,
]
TABLES_DIR = next((path for path in CANDIDATE_TABLE_DIRS if path.exists()), None)


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    if TABLES_DIR is None:
        raise FileNotFoundError(
            "Could not find reports/scania_project/tables in expected locations."
        )
    path = TABLES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def metric_card(label: str, value: str) -> None:
    st.metric(label, value)


def main() -> None:
    st.set_page_config(
        page_title="Scania Maintenance Prioritization",
        page_icon="",
        layout="wide",
    )

    st.title("Scania Maintenance Prioritization Prototype")
    st.caption(
        "Prototipo ligero para visualizar el score de falla, la prioridad operativa y la recomendacion de accion bajo la metodologia final del proyecto."
    )

    prioritization = load_csv("prioritization_output.csv")
    summary = load_csv("final_notebook_summary.csv")
    model_summary = load_csv("model_summary.csv")
    official_test = load_csv("official_test_results.csv")
    thresholds = load_csv("threshold_results.csv")
    importance = load_csv("feature_importance.csv")

    best_threshold = float(
        summary.loc[summary["item"] == "best_threshold_by_cost", "value"].iloc[0]
    )
    selected_model = summary.loc[summary["item"] == "selected_model", "value"].iloc[0]
    top_feature = summary.loc[summary["item"] == "most_important_feature", "value"].iloc[0]

    st.subheader("Project Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Selected model", selected_model)
    with col2:
        metric_card("Best threshold", f"{best_threshold:.2f}")
    with col3:
        metric_card("Top selected feature", top_feature)

    feature_strategy = summary.loc[
        summary["item"] == "feature_selection_strategy", "value"
    ].iloc[0]
    st.caption(
        f"Metodologia final: seleccion de caracteristicas = {feature_strategy}, modelo final = {selected_model}."
    )

    st.subheader("Operational View")
    left, right = st.columns([1, 2])

    with left:
        priority_options = ["todas"] + sorted(prioritization["priority_level"].dropna().unique().tolist())
        selected_priority = st.selectbox("Priority level", priority_options)

        action_options = ["todas"] + sorted(prioritization["recommended_action"].dropna().unique().tolist())
        selected_action = st.selectbox("Recommended action", action_options)

        score_min = float(prioritization["failure_score"].min())
        score_max = float(prioritization["failure_score"].max())
        score_range = st.slider(
            "Failure score range",
            min_value=0.0,
            max_value=1.0,
            value=(max(0.0, score_min), min(1.0, score_max)),
            step=0.01,
        )

    filtered = prioritization.copy()
    filtered = filtered[
        (filtered["failure_score"] >= score_range[0])
        & (filtered["failure_score"] <= score_range[1])
    ]
    if selected_priority != "todas":
        filtered = filtered[filtered["priority_level"] == selected_priority]
    if selected_action != "todas":
        filtered = filtered[filtered["recommended_action"] == selected_action]

    with right:
        st.write("Top prioritized records")
        st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)

    st.subheader("Priority Distribution")
    dist_col1, dist_col2 = st.columns(2)
    with dist_col1:
        priority_counts = prioritization["priority_level"].value_counts(dropna=False).reset_index()
        priority_counts.columns = ["priority_level", "count"]
        st.bar_chart(priority_counts.set_index("priority_level"))
    with dist_col2:
        action_counts = prioritization["recommended_action"].value_counts(dropna=False).reset_index()
        action_counts.columns = ["recommended_action", "count"]
        st.bar_chart(action_counts.set_index("recommended_action"))

    st.subheader("Model Comparison")
    st.dataframe(model_summary.round(4), use_container_width=True, hide_index=True)

    st.subheader("Official Test Results")
    st.dataframe(official_test.round(4), use_container_width=True, hide_index=True)

    st.subheader("Threshold Analysis")
    st.line_chart(thresholds.set_index("threshold")["cost"])

    st.subheader("Top Feature Importances")
    top_features = importance.head(15).copy().sort_values(by="importance", ascending=True)
    st.bar_chart(top_features.set_index("feature")["importance"])

    st.subheader("How to Read This Prototype")
    st.markdown(
        """
        - `failure_score`: probabilidad estimada de falla por el modelo.
        - `priority_level`: clasificacion operativa basada en score y umbral.
        - `recommended_action`: sugerencia de intervencion.
        - La salida corresponde a la fase metodologica consolidada del proyecto, no a la fase exploratoria inicial.
        - Un score alto no reemplaza la decision experta; sirve como apoyo para priorizar inspecciones.
        """
    )


if __name__ == "__main__":
    main()
