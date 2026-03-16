"""
Dashboard Ejecutivo — Transformación Digital Arçelik
OKRs Estratégicos: 6 Pivotes de Capacidades Dinámicas
Curso: Evolución Digital y Orquestación de Capacidades Dinámicas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arçelik | Digital Twin OKRs",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: #0f1923;
    color: #e0e6ef;
  }
  section[data-testid="stSidebar"] .stRadio label { color: #b0bec5 !important; }
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3 { color: #e0e6ef !important; }

  /* Main background */
  .stApp { background-color: #f7f9fc; }

  /* Metric cards */
  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border-left: 4px solid #1565C0;
    margin-bottom: 12px;
  }
  .metric-card.green { border-left-color: #2E7D32; }
  .metric-card.amber { border-left-color: #E65100; }
  .metric-card.red   { border-left-color: #B71C1C; }

  .metric-value { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
  .metric-label { font-size: 0.8rem; color: #607d8b; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }
  .metric-delta { font-size: 0.85rem; margin-top: 4px; }
  .delta-pos { color: #2E7D32; }
  .delta-neg { color: #B71C1C; }

  /* Section headers */
  .section-header {
    font-size: 1.4rem; font-weight: 700;
    color: #1a1a2e; margin: 24px 0 6px 0;
    border-bottom: 2px solid #1565C0;
    padding-bottom: 6px;
  }
  .pivote-badge {
    display: inline-block;
    background: #1565C0; color: white;
    border-radius: 20px; padding: 4px 14px;
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 0.06em; margin-bottom: 10px;
  }
  .okr-card {
    background: white; border-radius: 10px;
    padding: 18px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    margin-bottom: 14px;
  }
  .okr-title { font-size: 1rem; font-weight: 600; color: #1a1a2e; margin-bottom: 4px; }
  .okr-justif { font-size: 0.82rem; color: #546e7a; line-height: 1.5; margin-bottom: 10px; }
  .kr-row { display: flex; align-items: center; gap: 12px; margin: 6px 0; }
  .kr-label { font-size: 0.78rem; color: #607d8b; min-width: 200px; }

  /* Hero banner */
  .hero {
    background: linear-gradient(135deg, #0f1923 0%, #1565C0 100%);
    border-radius: 14px; padding: 32px 36px; color: white;
    margin-bottom: 24px;
  }
  .hero h1 { font-size: 1.9rem; font-weight: 700; margin: 0 0 6px 0; }
  .hero p  { font-size: 0.95rem; opacity: 0.85; margin: 0; }

  /* Env cards */
  .env-card {
    background: white; border-radius: 12px;
    padding: 22px 26px; margin-bottom: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .env-card h3 { font-size: 0.95rem; font-weight: 700; color: #1565C0; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 0.05em; }
  .env-card p  { font-size: 0.88rem; color: #37474f; line-height: 1.65; margin: 0; }

  /* Progress bars (custom) */
  .progress-wrap { background: #e8eaf6; border-radius: 6px; height: 8px; width: 100%; }
  .progress-fill { height: 8px; border-radius: 6px; transition: width 0.4s ease; }
</style>
""", unsafe_allow_html=True)

# ── Simulated data ────────────────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

PIVOTES = {
    "🔗 Alineamiento Dinámico": "AD",
    "💡 Liderazgo Digital":     "LD",
    "👤 Innovación al Cliente":  "IC",
    "⚡ Agilidad Operativa":     "AO",
    "📊 Decisiones por Datos":   "DD",
    "🤝 Ecosistemas de Colab.":  "EC",
}

COLORS = {
    "AD": "#1565C0",
    "LD": "#6A1B9A",
    "IC": "#00695C",
    "AO": "#E65100",
    "DD": "#0277BD",
    "EC": "#4E342E",
}

def status_color(pct):
    if pct >= 80:  return "green"
    if pct >= 50:  return "amber"
    return "red"

def gauge(value, title, color="#1565C0", suffix="%"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 28, "family": "Inter"}},
        title={"text": title, "font": {"size": 13, "family": "Inter", "color": "#546e7a"}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 10}},
            "bar": {"color": color},
            "bgcolor": "#f0f4f8",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50],  "color": "#ffebee"},
                {"range": [50, 80], "color": "#fff3e0"},
                {"range": [80, 100],"color": "#e8f5e9"},
            ],
            "threshold": {"line": {"color": "#1a1a2e", "width": 3}, "thickness": 0.75, "value": 80},
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="white")
    return fig

def bar_progress(labels, values, targets, color, title):
    pct = [min(v/t*100, 100) for v, t in zip(values, targets)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pct, y=labels, orientation='h',
        marker_color=[color if p >= 80 else ("#FFA726" if p >= 50 else "#EF5350") for p in pct],
        text=[f"{p:.0f}%" for p in pct],
        textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title=title, xaxis=dict(range=[0, 110], showgrid=False, zeroline=False, title="% hacia meta"),
        yaxis=dict(showgrid=False),
        height=max(200, len(labels)*55 + 80),
        margin=dict(l=10, r=60, t=50, b=20),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=12),
    )
    fig.add_vline(x=80, line_dash="dash", line_color="#546e7a", opacity=0.4)
    return fig

def line_trend(months, series_dict, title, color_map):
    fig = go.Figure()
    for name, vals in series_dict.items():
        fig.add_trace(go.Scatter(
            x=months, y=vals, mode="lines+markers", name=name,
            line=dict(color=color_map.get(name, "#1565C0"), width=2),
            marker=dict(size=6),
        ))
    fig.update_layout(
        title=title, height=280,
        margin=dict(l=10, r=10, t=50, b=20),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f4f8"),
    )
    return fig

# ── Monthly trend data ────────────────────────────────────────────────────────
months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

def smooth_series(start, end, noise=0.5):
    base = np.linspace(start, end, 12)
    return np.clip(base + np.random.normal(0, noise, 12), 0, 100).tolist()

# Scrap ratio (lower is better) — from 6% toward 1%
scrap_pre  = [6.8, 7.2, 6.1, 5.8, 6.3, 5.5, 2.1, 1.8, 1.5, 1.3, 1.1, 1.0]
# OEE (higher is better) — from 70% toward 88%
oee_series = [70, 71, 69, 72, 71, 70, 82, 85, 87, 88, 89, 90]
# Plastic savings (cumulative tons)
plastic_savings = [0, 0, 0, 0, 0, 0, 133, 266, 400, 533, 666, 800]

# ── OKR progress data ─────────────────────────────────────────────────────────
okr_data = {
    "AD": {
        "title": "Alineamiento Dinámico",
        "color": COLORS["AD"],
        "okrs": [
            {
                "id": "OBJ-AD-01",
                "title": "Consolidar visión digital compartida",
                "justif": "El éxito del digital twin dependió de que múltiples equipos compartieran objetivos comunes. Sin alineamiento, los equipos operaban con supuestos distintos sobre el proceso.",
                "why_measure": "Sin una visión digital medida y verificada, el alineamiento es solo declarativo. En el caso Arçelik, los silos entre IT, producción y automatización generaron fricciones reales. Medir este OKR permite detectar temprano qué unidades aún no han internalizado la hoja de ruta y corregir antes de que la brecha afecte el despliegue global.",
                "krs": [
                    {"id": "KR-AD-01.1", "label": "Plantas con roadmap digital aprobado (%)", "current": 62, "target": 100, "owner": "CDO", "cadencia": "Semestral"},
                    {"id": "KR-AD-01.2", "label": "Sesiones cross-funcionales realizadas", "current": 18, "target": 24, "owner": "PMO", "cadencia": "Mensual"},
                    {"id": "KR-AD-01.3", "label": "KPIs vinculados a obj. digitales (%)", "current": 71, "target": 85, "owner": "Dir. Estrategia", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-AD-02",
                "title": "Escalar digital twin a 32 líneas globales",
                "justif": "El twin fue probado en una planta. El escalamiento global requiere que cada región acepte y ejecute el mismo modelo operativo digital.",
                "why_measure": "El piloto exitoso en una planta no garantiza la replicabilidad global. Medir el avance del escalamiento permite identificar qué plantas enfrentan barreras técnicas, culturales o de infraestructura antes de comprometer presupuesto. Sin esta métrica, la alta gerencia opera a ciegas sobre el estado real del despliegue.",
                "krs": [
                    {"id": "KR-AD-02.1", "label": "Plantas con DT operativo / 8 totales", "current": 2, "target": 8, "owner": "Dir. Manufactura Global", "cadencia": "Trimestral"},
                    {"id": "KR-AD-02.2", "label": "Parámetros estandarizados entre plantas (%)", "current": 58, "target": 90, "owner": "Eq. Simulación", "cadencia": "Semestral"},
                    {"id": "KR-AD-02.3", "label": "Reducción CV del OEE entre plantas (%)", "current": 14, "target": 30, "owner": "Dir. Operaciones", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-AD-03",
                "title": "Institucionalizar gobernanza digital",
                "justif": "La gobernanza flexible reduce fricciones futuras en proyectos I4.0, balanceando la rigidez administrativa de Arçelik con la agilidad requerida.",
                "why_measure": "El caso documenta que los tiempos de aprobación fueron uno de los principales cuellos de botella del proyecto. Medir la velocidad y cobertura de la gobernanza digital revela si la organización está reduciendo su inercia burocrática o si los mismos obstáculos seguirán afectando futuros proyectos de transformación.",
                "krs": [
                    {"id": "KR-AD-03.1", "label": "Decisiones digitales por comité (%)", "current": 80, "target": 100, "owner": "C-Suite", "cadencia": "Trimestral"},
                    {"id": "KR-AD-03.2", "label": "Reducción tiempo aprobación proyectos (%)", "current": 28, "target": 40, "owner": "PMO Corp.", "cadencia": "Trimestral"},
                    {"id": "KR-AD-03.3", "label": "NPS interno equipos digitales", "current": 32, "target": 40, "owner": "Dir. RRHH", "cadencia": "Semestral"},
                ],
            },
        ],
    },
    "LD": {
        "title": "Liderazgo Digital",
        "color": COLORS["LD"],
        "okrs": [
            {
                "id": "OBJ-LD-01",
                "title": "Desarrollar masa crítica de líderes digitales",
                "justif": "Sin líderes capaces de interpretar datos de sensores, metodologías ágiles y colaboración con startups, el proyecto no habría avanzado.",
                "why_measure": "Las transformaciones digitales fallan más por déficit de liderazgo que por déficit tecnológico. Medir la certificación y retención de líderes digitales permite anticipar si Arçelik tiene el capital humano suficiente para sostener el programa I4.0 a escala global, o si depende de pocos individuos irremplazables.",
                "krs": [
                    {"id": "KR-LD-01.1", "label": "Gerentes certificados en liderazgo digital (%)", "current": 42, "target": 70, "owner": "CPO / Atölye 4.0", "cadencia": "Semestral"},
                    {"id": "KR-LD-01.2", "label": "Líderes ágiles certificados activos", "current": 28, "target": 50, "owner": "PMO", "cadencia": "Trimestral"},
                    {"id": "KR-LD-01.3", "label": "Retención perfiles digitales clave (%)", "current": 88, "target": 90, "owner": "CPO", "cadencia": "Anual"},
                ],
            },
            {
                "id": "OBJ-LD-02",
                "title": "Posicionar Arçelik como referente digital global",
                "justif": "Arçelik ya fue reconocido como Global Lighthouse Factory en Rumania. El liderazgo digital externo refuerza la marca y atrae talento.",
                "krs": [
                    {"id": "KR-LD-02.1", "label": "Plantas adicionales certificadas WEF", "current": 0, "target": 2, "owner": "CEO / Dir. Estrategia", "cadencia": "Anual"},
                    {"id": "KR-LD-02.2", "label": "Publicaciones/presentaciones I4.0", "current": 4, "target": 6, "owner": "Dir. Comunicaciones", "cadencia": "Semestral"},
                    {"id": "KR-LD-02.3", "label": "Vacantes digitales cubiertas en 60 días (%)", "current": 68, "target": 80, "owner": "CPO", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-LD-03",
                "title": "Normalizar cultura de experimentación digital",
                "justif": "Arçelik intentó ML y FEA antes del digital twin. La capacidad de pivotar sin abandonar el proyecto debe institucionalizarse.",
                "why_measure": "Una cultura que no mide su propia capacidad de experimentar tiende a recaer en el conservadurismo. Cuantificar el número de experimentos lanzados, la velocidad de decisión en contextos de incertidumbre y el clima de innovación permite a la alta gerencia saber si la mentalidad ágil está arraigando o si fue un evento puntual.",
                "krs": [
                    {"id": "KR-LD-03.1", "label": "Experimentos digitales lanzados", "current": 9, "target": 12, "owner": "Dir. Atölye 4.0", "cadencia": "Trimestral"},
                    {"id": "KR-LD-03.2", "label": "Tiempo identificación → piloto (días)", "current": 110, "target": 90, "owner": "PMO / CTO", "cadencia": "Trimestral"},
                    {"id": "KR-LD-03.3", "label": "Score cultura de innovación (1–10)", "current": 6.8, "target": 7.5, "owner": "CPO", "cadencia": "Anual"},
                ],
            },
        ],
    },
    "IC": {
        "title": "Innovación Centrada en el Cliente",
        "color": COLORS["IC"],
        "okrs": [
            {
                "id": "OBJ-IC-01",
                "title": "Reducir defectos que impactan calidad percibida",
                "justif": "Los problemas de termoformado generaban defectos visibles en el producto final. La reducción del scrap de 5–8% a 1–2% es una mejora directa en experiencia del cliente.",
                "why_measure": "La calidad del proceso interno solo genera valor si se traduce en menos defectos percibidos por el cliente. Medir este OKR cierra el ciclo entre la operación fabril y la satisfacción del mercado. Sin este vínculo medido, los ahorros operativos del digital twin quedan desconectados del propósito estratégico de la empresa.",
                "krs": [
                    {"id": "KR-IC-01.1", "label": "Scrap ratio líneas termoformado (%)", "current": 1.4, "target": 1.0, "owner": "Dir. Calidad", "cadencia": "Mensual"},
                    {"id": "KR-IC-01.2", "label": "Reducción reclamaciones garantía (%)", "current": 38, "target": 50, "owner": "Dir. Servicio", "cadencia": "Trimestral"},
                    {"id": "KR-IC-01.3", "label": "NPS calidad de construcción (delta pts)", "current": 7, "target": 10, "owner": "Dir. Marketing", "cadencia": "Semestral"},
                ],
            },
            {
                "id": "OBJ-IC-02",
                "title": "Acelerar lanzamiento de nuevos modelos",
                "justif": "Cada nuevo refrigerador requiere un nuevo modelo FEM. El digital twin debe convertirse en ventaja competitiva para acortar el time-to-market.",
                "why_measure": "La velocidad de innovación de producto es un diferenciador competitivo crítico en el mercado de electrodomésticos. Medir el time-to-production y la tasa de éxito en primeros runs permite cuantificar si el digital twin está generando ventaja competitiva real, más allá del ahorro en materiales.",
                "krs": [
                    {"id": "KR-IC-02.1", "label": "Reducción tiempo setup nuevo modelo (%)", "current": 33, "target": 50, "owner": "Dir. Ingeniería", "cadencia": "Por proyecto"},
                    {"id": "KR-IC-02.2", "label": "Nuevos modelos con calidad en 1er run (%)", "current": 78, "target": 90, "owner": "Dir. Ing. Proceso", "cadencia": "Por lanzamiento"},
                    {"id": "KR-IC-02.3", "label": "Reducción time-to-production (%)", "current": 21, "target": 30, "owner": "Dir. R&D", "cadencia": "Por proyecto"},
                ],
            },
            {
                "id": "OBJ-IC-03",
                "title": "Integrar voz del cliente en el digital twin",
                "justif": "El siguiente nivel de madurez es cerrar el ciclo incorporando datos de campo y retroalimentación del cliente para mejorar continuamente el modelo.",
                "why_measure": "Un digital twin que solo aprende del proceso interno tiene un techo de mejora. Medir la integración de datos de campo en el modelo permite evaluar si Arçelik avanza hacia un sistema de aprendizaje continuo, donde cada falla en campo retroalimenta el modelo y previene recurrencias en fábrica.",
                "krs": [
                    {"id": "KR-IC-03.1", "label": "Modelos con datos de campo integrados (%)", "current": 22, "target": 60, "owner": "Dir. R&D / Analytics", "cadencia": "Semestral"},
                    {"id": "KR-IC-03.2", "label": "Tiempo defecto campo → ajuste DT (días)", "current": 28, "target": 15, "owner": "Dir. Calidad / IT", "cadencia": "Trimestral"},
                    {"id": "KR-IC-03.3", "label": "Mejoras proceso originadas en datos cliente", "current": 5, "target": 8, "owner": "Dir. Mejora Continua", "cadencia": "Trimestral"},
                ],
            },
        ],
    },
    "AO": {
        "title": "Agilidad Operativa",
        "color": COLORS["AO"],
        "okrs": [
            {
                "id": "OBJ-AO-01",
                "title": "Institucionalizar metodologías ágiles",
                "justif": "El modelo waterfall era inadecuado para alta incertidumbre tecnológica. La agilidad fue la decisión que salvó presupuesto y cronograma del proyecto.",
                "why_measure": "La adopción de metodologías ágiles declarada en un documento no equivale a capacidad organizacional real. Medir la velocidad de sprint, la desviación de presupuesto y la cobertura ágil en proyectos activos permite determinar si la organización ha internalizado el método o si solo lo aplica superficialmente bajo presión.",
                "krs": [
                    {"id": "KR-AO-01.1", "label": "Proyectos digitales con metodología ágil (%)", "current": 72, "target": 90, "owner": "PMO Corp.", "cadencia": "Trimestral"},
                    {"id": "KR-AO-01.2", "label": "Incremento velocidad de sprint (%)", "current": 16, "target": 25, "owner": "PMO / Líderes", "cadencia": "Quincenal"},
                    {"id": "KR-AO-01.3", "label": "Proyectos dentro de ±10% ppto/crono (%)", "current": 68, "target": 80, "owner": "PMO / CFO", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-AO-02",
                "title": "Reducir tiempo de respuesta operativa",
                "justif": "El valor del digital twin no está solo en detectar problemas, sino en la velocidad de respuesta. El sistema tiene dos modos: manual y automático.",
                "why_measure": "Un sistema de detección sin respuesta rápida no genera valor operativo. Medir la latencia desde la alerta hasta la corrección —y el porcentaje de correcciones automáticas— revela el nivel de madurez real del sistema. Es el indicador que separa un digital twin informativo de uno verdaderamente operativo.",
                "krs": [
                    {"id": "KR-AO-02.1", "label": "Tiempo alerta → corrección manual (min)", "current": 42, "target": 30, "owner": "Dir. Operaciones", "cadencia": "Mensual"},
                    {"id": "KR-AO-02.2", "label": "Correcciones ejecutadas automáticamente (%)", "current": 48, "target": 70, "owner": "Dir. Automatización", "cadencia": "Trimestral"},
                    {"id": "KR-AO-02.3", "label": "Incremento MTBF líneas con DT (%)", "current": 27, "target": 40, "owner": "Dir. Mantenimiento", "cadencia": "Mensual"},
                ],
            },
            {
                "id": "OBJ-AO-03",
                "title": "Optimizar consumo de materiales en tiempo real",
                "justif": "El ahorro de 1,600 toneladas anuales ($2M+) fue resultado del control en tiempo real. Escalar requiere sistematizar el control adaptativo en todas las líneas.",
                "why_measure": "Este OKR conecta directamente la transformación digital con el P&L de la empresa. Medir el ahorro acumulado y la reducción de consumo por unidad producida permite justificar ante el CFO y el consejo la inversión en el programa de digital twins con evidencia financiera y ambiental cuantificada.",
                "krs": [
                    {"id": "KR-AO-03.1", "label": "Reducción plástico por unidad (% anual)", "current": 5.8, "target": 8.0, "owner": "Dir. Operaciones", "cadencia": "Mensual"},
                    {"id": "KR-AO-03.2", "label": "Ahorro acumulado materiales (USD M)", "current": 2.4, "target": 6.0, "owner": "CFO", "cadencia": "Trimestral"},
                    {"id": "KR-AO-03.3", "label": "Reducción kWh/ton plástico procesado (%)", "current": 9, "target": 15, "owner": "Dir. Sostenibilidad", "cadencia": "Mensual"},
                ],
            },
        ],
    },
    "DD": {
        "title": "Decisiones Basadas en Datos",
        "color": COLORS["DD"],
        "okrs": [
            {
                "id": "OBJ-DD-01",
                "title": "Construir infraestructura de datos robusta",
                "justif": "Sin la infraestructura PLC/IoT existente, el digital twin no habría sido posible. Formalizar y escalar esta infraestructura es prerequisito para decisiones basadas en datos.",
                "why_measure": "Una decisión basada en datos de mala calidad o con alta latencia puede ser más dañina que una decisión intuitiva. Medir la cobertura de sensores, el uptime del pipeline y la latencia de datos asegura que el digital twin opere sobre información confiable. Sin estas métricas, la precisión del modelo es una incógnita.",
                "krs": [
                    {"id": "KR-DD-01.1", "label": "Parámetros críticos monitoreados en RT (%)", "current": 81, "target": 95, "owner": "Dir. IT", "cadencia": "Trimestral"},
                    {"id": "KR-DD-01.2", "label": "Uptime infraestructura de datos (%)", "current": 98.7, "target": 99.5, "owner": "CTO", "cadencia": "Mensual"},
                    {"id": "KR-DD-01.3", "label": "Latencia captura → dashboard (seg)", "current": 18, "target": 10, "owner": "Dir. IT / Arquitectura", "cadencia": "Mensual"},
                ],
            },
            {
                "id": "OBJ-DD-02",
                "title": "Transformar conocimiento tácito en modelos explícitos",
                "justif": "El conocimiento tácito de operadores era el principal activo no codificado del proceso. Digitalizarlo fue una de las contribuciones más importantes del proyecto.",
                "why_measure": "El conocimiento tácito no medido es un riesgo de continuidad operativa: si un operador experto se va, el conocimiento se va con él. Medir qué porcentaje del saber-hacer del proceso ha sido codificado en el modelo permite gestionar este riesgo y cuantificar el avance real de la digitalización del capital intelectual.",
                "krs": [
                    {"id": "KR-DD-02.1", "label": "Procedimientos críticos codificados en DT (%)", "current": 55, "target": 80, "owner": "Dir. Ing. Proceso", "cadencia": "Trimestral"},
                    {"id": "KR-DD-02.2", "label": "MAPE del digital twin vs. valores reales", "current": 7.2, "target": 5.0, "owner": "Eq. Simulación", "cadencia": "Mensual"},
                    {"id": "KR-DD-02.3", "label": "Ajustes guiados por sistema vs. operador (%)", "current": 48, "target": 65, "owner": "Dir. Operaciones", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-DD-03",
                "title": "Desarrollar capacidades de analytics avanzado",
                "justif": "El intento inicial de ML falló por limitaciones en feature engineering. Internalizar esta capacidad es crítico para la autonomía analítica de Arçelik.",
                "why_measure": "Depender de Simularge para todo el feature engineering crea una vulnerabilidad estratégica de largo plazo. Medir la cantidad de data scientists internos certificados, las iteraciones de mejora del modelo y el porcentaje de detección predictiva permite evaluar si Arçelik está construyendo soberanía analítica o perpetuando la dependencia externa.",
                "krs": [
                    {"id": "KR-DD-03.1", "label": "Data scientists certificados internos", "current": 11, "target": 20, "owner": "CPO / CTO", "cadencia": "Semestral"},
                    {"id": "KR-DD-03.2", "label": "Iteraciones mejora de modelo por año/planta", "current": 2, "target": 4, "owner": "Dir. R&D", "cadencia": "Trimestral"},
                    {"id": "KR-DD-03.3", "label": "Defectos detectados predictivamente (%)", "current": 52, "target": 75, "owner": "Dir. Calidad / Analytics", "cadencia": "Mensual"},
                ],
            },
        ],
    },
    "EC": {
        "title": "Ecosistemas de Colaboración",
        "color": COLORS["EC"],
        "okrs": [
            {
                "id": "OBJ-EC-01",
                "title": "Fortalecer ecosistema startup-academia-empresa",
                "justif": "La conexión con ITU Çekirdek y Simularge fue más efectiva que contratar a un vendor establecido. Este modelo debe convertirse en capacidad sistemática.",
                "why_measure": "Sin métricas, el ecosistema de colaboración queda como un logro puntual en lugar de convertirse en una capacidad organizacional sostenible. Medir el número de startups activas, los proyectos co-desarrollados y el ROI comparativo permite demostrar al consejo que la apuesta por el ecosistema genera más valor que el modelo transaccional tradicional.",
                "krs": [
                    {"id": "KR-EC-01.1", "label": "Startups activas en proyectos colaborativos", "current": 7, "target": 15, "owner": "Dir. Atölye 4.0", "cadencia": "Trimestral"},
                    {"id": "KR-EC-01.2", "label": "Proyectos co-desarrollados con universidades", "current": 4, "target": 8, "owner": "Dir. R&D", "cadencia": "Trimestral"},
                    {"id": "KR-EC-01.3", "label": "ROI proyectos con startups vs. internos (x)", "current": 1.3, "target": 1.5, "owner": "CFO / Dir. Innovación", "cadencia": "Anual"},
                ],
            },
            {
                "id": "OBJ-EC-02",
                "title": "Desarrollar modelo replicable empresa-startup",
                "justif": "Arçelik tenía 'reglas estrictas y procedimientos rígidos' para colaborar con startups. Reducir estas fricciones es una capacidad organizacional estratégica.",
                "why_measure": "La fricción en el proceso de onboarding de startups no solo ralentiza proyectos: disuade al mejor talento emprendedor de querer trabajar con Arçelik. Medir el tiempo de negociación, la adopción del playbook y la satisfacción de los startups socios permite cuantificar si la organización está volviéndose genuinamente colaborativa o solo aparentándolo.",
                "krs": [
                    {"id": "KR-EC-02.1", "label": "Tiempo contacto → acuerdo startup (días)", "current": 68, "target": 45, "owner": "Dir. Legal / PMO", "cadencia": "Por proyecto"},
                    {"id": "KR-EC-02.2", "label": "Proyectos con playbook estandarizado (%)", "current": 55, "target": 100, "owner": "Dir. Atölye 4.0", "cadencia": "Trimestral"},
                    {"id": "KR-EC-02.3", "label": "Satisfacción startups socios (1–10)", "current": 7.2, "target": 8.0, "owner": "Dir. Atölye 4.0", "cadencia": "Anual"},
                ],
            },
            {
                "id": "OBJ-EC-03",
                "title": "Posicionar Arçelik como hub de innovación manufacturera",
                "justif": "La relación con ITU Çekirdek y el reconocimiento Global Lighthouse posiciona a Arçelik como polo gravitacional del ecosistema. Esta posición debe gestionarse activamente.",
                "why_measure": "El posicionamiento como hub de innovación no es un objetivo de relaciones públicas: es una palanca de acceso a co-financiamiento externo, talento de élite y nuevas colaboraciones. Medir el porcentaje de proyectos con financiamiento externo y la presencia en rankings internacionales permite evaluar el retorno estratégico de esta inversión de reputación.",
                "krs": [
                    {"id": "KR-EC-03.1", "label": "Proyectos con co-financiamiento externo (%)", "current": 18, "target": 30, "owner": "Dir. R&D / CFO", "cadencia": "Anual"},
                    {"id": "KR-EC-03.2", "label": "Startups escaladas con apoyo Arçelik", "current": 2, "target": 5, "owner": "Dir. Atölye 4.0", "cadencia": "Anual"},
                    {"id": "KR-EC-03.3", "label": "Rankings internacionales como caso I4.0", "current": 1, "target": 3, "owner": "CEO / Dir. Estrategia", "cadencia": "Anual"},
                ],
            },
        ],
    },
}

# ── Helper: compute OKR overall progress ─────────────────────────────────────
def kr_progress(kr):
    """Returns 0–100% regardless of whether higher or lower is better."""
    c, t = kr["current"], kr["target"]
    # For time-based KRs where lower is better (days, minutes, %, MAPE)
    lower_better_keywords = ["tiempo", "latencia", "mape", "scrap"]
    lbl = kr["label"].lower()
    if any(k in lbl for k in lower_better_keywords):
        # Progress = how much we've improved toward target from a notional "bad" baseline
        # Use a simple inversion: baseline assumed to be 2x target or current (whichever larger)
        baseline = max(c * 1.5, t * 2)
        progress = (baseline - c) / (baseline - t) * 100
    else:
        progress = c / t * 100
    return round(min(max(progress, 0), 100), 1)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 Arçelik Digital Twin")
    st.markdown("### Dashboard OKRs Estratégicos")
    st.markdown("---")
    pages = ["🏠 Ambiente del Problema", "📊 Resumen Ejecutivo"] + list(PIVOTES.keys())
    page = st.radio("Navegación", pages, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(
        "**Caso:** Arçelik × Simularge  \n"
        "**Curso:** Evolución Digital y  \nOrquestación de Capacidades Dinámicas  \n"
        "**Año:** 2024"
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — AMBIENTE DEL PROBLEMA
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Ambiente del Problema":
    st.markdown("""
    <div class="hero">
      <h1>🏭 Arçelik × Simularge — Digital Twin</h1>
      <p>Digitalización del Proceso de Termoformado · Caso de Transformación Industrial</p>
    </div>
    """, unsafe_allow_html=True)

    # Top KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card green"><div class="metric-label">Ahorro Anual</div><div class="metric-value">$2M+</div><div class="metric-delta delta-pos">↑ Año 1 post-implementación</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card green"><div class="metric-label">Plástico Ahorrado</div><div class="metric-value">1,600 t</div><div class="metric-delta delta-pos">↑ por año</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card green"><div class="metric-label">Scrap Ratio</div><div class="metric-value">5–8% → 1–2%</div><div class="metric-delta delta-pos">↓ Reducción significativa</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card green"><div class="metric-label">OEE</div><div class="metric-value">68–75% → 82–92%</div><div class="metric-delta delta-pos">↑ Mejora de eficiencia</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Ambiente del Problema</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown("""
        <div class="env-card">
          <h3>👤 Tomador de Decisiones</h3>
          <p>
            <strong>Director de Tecnologías de Producción — Arçelik A.Ş.</strong><br><br>
            Equipo liderado por la Dirección de Manufactura y el Centro de Competencias
            <em>Atölye 4.0</em>, con participación de los grupos de manufactura inteligente,
            producción, ingeniería y tecnologías de proceso y materiales.<br><br>
            Arçelik es el tercer fabricante de electrodomésticos más grande de Europa,
            con 30,000 empleados, 12 marcas y 23 plantas en el mundo. El desafío fue
            liderado desde su unidad de innovación industrial establecida en 2016.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="env-card">
          <h3>📋 Tarea Estratégica</h3>
          <p>
            <strong>Decisión central:</strong> Desarrollar e implementar un gemelo digital
            (<em>digital twin</em>) del proceso de termoformado para reducir el consumo de
            plástico, disminuir el índice de desperdicio y mejorar la calidad del producto.<br><br>
            <strong>Transformación requerida:</strong><br>
            • Digitalizar un proceso gobernado por conocimiento tácito de operadores.<br>
            • Elegir entre vendor establecido vs. colaboración con startup especializada.<br>
            • Adoptar metodologías ágiles en una organización con estructuras rígidas.<br>
            • Diseñar un modelo de despliegue global desde un piloto de una sola planta.<br><br>
            <strong>Objetivo:</strong> Integrar ingeniería de simulación, sensores IoT y
            control PLC en tiempo real para optimizar los 32 equipos de termoformado en
            9 ubicaciones mundiales.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="env-card">
          <h3>🌍 Entorno Estratégico</h3>
          <p>
            <strong>Industria:</strong> Manufactura de bienes duraderos (electrodomésticos).
            Sector altamente competitivo con presión constante sobre costos, calidad y
            sostenibilidad ambiental.<br><br>
            <strong>Presión competitiva:</strong> Necesidad de diferenciación en calidad
            y eficiencia frente a competidores globales. Arçelik compite en 150+ países
            bajo 12 marcas. La eficiencia de manufactura es un diferenciador clave.<br><br>
            <strong>Cambio tecnológico:</strong> Emergencia del paradigma Industria 4.0.
            Los gemelos digitales aparecen como tecnología habilitadora crítica para la
            manufactura inteligente. Gartner proyectaba que el 50% de las empresas
            industriales adoptarían DTs para 2021.<br><br>
            <strong>Mercado:</strong> Producción anual de ~20 millones de unidades.
            Los refrigeradores representan el 35% de la producción. El termoformado
            consume >20,000 toneladas de plástico/año — una palanca de costo y
            sostenibilidad significativa.<br><br>
            <strong>Presión regulatoria / ambiental:</strong> Inclusión en el Dow Jones
            Sustainability Index desde 2017. Premio Cero Residuos del Ministerio de Medio
            Ambiente de Turquía. Alineamiento con ODS 12 de Naciones Unidas
            (Producción y Consumo Responsables).<br><br>
            <strong>Cultura organizacional:</strong> Tensión entre la inercia estructural
            de una gran corporación (procesos rígidos, aprobaciones múltiples) y la
            necesidad de agilidad para proyectos tecnológicos con alta incertidumbre.
            El rechazo al modelo waterfall y la adopción de metodologías ágiles fue
            un cambio cultural deliberado.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # Timeline
    st.markdown('<div class="section-header">Línea de Tiempo del Proyecto</div>', unsafe_allow_html=True)
    timeline_data = {
        "Hito": ["Fundación Arçelik", "Establecimiento Atölye 4.0", "Fundación Simularge en ITU Çekirdek",
                  "Inicio proyecto DT", "Lighthouse Factory Rumanía (WEF)", "Implementación DT piloto",
                  "Ahorro $2M+ confirmado", "Plan despliegue global"],
        "Año": [1955, 2016, 2017, 2019, 2019, 2020, 2020, 2021],
        "Categoría": ["Empresa", "Innovación", "Ecosistema", "Proyecto",
                       "Reconocimiento", "Proyecto", "Resultado", "Estrategia"],
    }
    df_tl = pd.DataFrame(timeline_data)
    col_map = {"Empresa": "#1565C0", "Innovación": "#6A1B9A", "Ecosistema": "#4E342E",
                "Proyecto": "#E65100", "Reconocimiento": "#2E7D32", "Resultado": "#00695C",
                "Estrategia": "#0277BD"}
    fig_tl = px.scatter(df_tl, x="Año", y="Hito", color="Categoría",
                         color_discrete_map=col_map, size_max=12,
                         title="Hitos Estratégicos del Programa de Transformación Digital")
    fig_tl.update_traces(marker=dict(size=14))
    fig_tl.update_layout(height=320, paper_bgcolor="white", plot_bgcolor="white",
                          font=dict(family="Inter", size=12),
                          margin=dict(l=10, r=10, t=50, b=20),
                          xaxis=dict(showgrid=True, gridcolor="#f0f4f8"),
                          yaxis=dict(showgrid=False))
    st.plotly_chart(fig_tl, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RESUMEN EJECUTIVO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Resumen Ejecutivo":
    st.markdown("""
    <div class="hero">
      <h1>📊 Resumen Ejecutivo — Estado de OKRs</h1>
      <p>Vista consolidada de los 6 Pivotes Estratégicos · 18 Objetivos · 54 Key Results</p>
    </div>
    """, unsafe_allow_html=True)

    # Compute overall progress per pivote
    pivote_scores = {}
    for code, data in okr_data.items():
        all_pcts = []
        for okr in data["okrs"]:
            for kr in okr["krs"]:
                all_pcts.append(kr_progress(kr))
        pivote_scores[code] = round(np.mean(all_pcts), 1)

    # Spider / radar chart
    codes = list(pivote_scores.keys())
    names = [okr_data[c]["title"] for c in codes]
    vals  = [pivote_scores[c] for c in codes]
    vals_closed = vals + [vals[0]]
    names_closed = names + [names[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_closed, theta=names_closed,
        fill='toself', fillcolor='rgba(21,101,192,0.15)',
        line=dict(color='#1565C0', width=2),
        name="Progreso actual",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[80]*len(names_closed), theta=names_closed,
        line=dict(color='#2E7D32', width=1, dash='dash'),
        name="Meta mínima (80%)",
        mode="lines",
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=11)),
        ),
        showlegend=True,
        height=420,
        paper_bgcolor="white",
        font=dict(family="Inter"),
        title="Progreso Global por Pivote Estratégico",
        margin=dict(l=60, r=60, t=60, b=40),
    )

    col_r1, col_r2 = st.columns([1.2, 1])
    with col_r1:
        st.plotly_chart(fig_radar, use_container_width=True)
    with col_r2:
        st.markdown("### Estado por Pivote")
        for code, score in pivote_scores.items():
            color = COLORS[code]
            sc = status_color(score)
            dot = "🟢" if sc == "green" else ("🟡" if sc == "amber" else "🔴")
            st.markdown(
                f"**{dot} {okr_data[code]['title']}**  \n"
                f"Progreso: **{score}%**"
            )
            prog_color = "#2E7D32" if score >= 80 else ("#E65100" if score >= 50 else "#B71C1C")
            st.markdown(
                f'<div class="progress-wrap"><div class="progress-fill" style="width:{score}%;background:{prog_color};"></div></div>',
                unsafe_allow_html=True,
            )
            st.markdown("")

    # KR heatmap
    st.markdown('<div class="section-header">Mapa de Calor — Progreso de Key Results</div>', unsafe_allow_html=True)
    heat_rows = []
    for code, data in okr_data.items():
        for okr in data["okrs"]:
            for kr in okr["krs"]:
                heat_rows.append({
                    "Pivote": data["title"][:22],
                    "OKR": okr["id"],
                    "KR": kr["id"],
                    "Progreso": kr_progress(kr),
                })
    df_heat = pd.DataFrame(heat_rows)
    pivot_heat = df_heat.pivot(index="KR", columns="Pivote", values="Progreso").fillna(0)
    fig_heat = px.imshow(
        pivot_heat,
        color_continuous_scale=[[0,"#ffebee"],[0.5,"#fff3e0"],[0.8,"#e8f5e9"],[1,"#1565C0"]],
        zmin=0, zmax=100,
        title="Progreso (%) de cada KR por Pivote Estratégico",
        aspect="auto",
    )
    fig_heat.update_layout(height=600, paper_bgcolor="white", font=dict(family="Inter", size=11),
                            margin=dict(l=10, r=10, t=50, b=20),
                            coloraxis_colorbar=dict(title="% Progreso"))
    st.plotly_chart(fig_heat, use_container_width=True)

    # Operational results
    st.markdown('<div class="section-header">Resultados Operativos Clave — Evolución Mensual</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig_scrap = go.Figure()
        fig_scrap.add_trace(go.Scatter(x=months, y=scrap_pre, fill='tozeroy',
                                        line=dict(color="#EF5350", width=2), name="Scrap Ratio (%)"))
        fig_scrap.add_hline(y=2, line_dash="dash", line_color="#2E7D32", annotation_text="Meta: ≤2%")
        fig_scrap.update_layout(title="Scrap Ratio — Termoformado", height=260,
                                  paper_bgcolor="white", plot_bgcolor="white",
                                  font=dict(family="Inter", size=12),
                                  margin=dict(l=10, r=10, t=50, b=20),
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f4f8"))
        st.plotly_chart(fig_scrap, use_container_width=True)
    with c2:
        fig_oee = go.Figure()
        fig_oee.add_trace(go.Scatter(x=months, y=oee_series, fill='tozeroy',
                                      line=dict(color="#1565C0", width=2), name="OEE (%)"))
        fig_oee.add_hline(y=82, line_dash="dash", line_color="#2E7D32", annotation_text="Meta: ≥82%")
        fig_oee.update_layout(title="OEE — Eficiencia Global de Equipos", height=260,
                               paper_bgcolor="white", plot_bgcolor="white",
                               font=dict(family="Inter", size=12),
                               margin=dict(l=10, r=10, t=50, b=20),
                               xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f4f8"))
        st.plotly_chart(fig_oee, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PIVOTE PAGES
# ══════════════════════════════════════════════════════════════════════════════
else:
    # Identify pivote
    pcode = PIVOTES.get(page)
    if pcode and pcode in okr_data:
        pdata = okr_data[pcode]
        color = pdata["color"]

        # Hero
        st.markdown(f"""
        <div class="hero" style="background: linear-gradient(135deg, #0f1923 0%, {color} 100%);">
          <h1>{page}</h1>
          <p>Pivote Estratégico · {len(pdata['okrs'])} Objetivos · {len(pdata['okrs'])*3} Key Results</p>
        </div>
        """, unsafe_allow_html=True)

        # Pivote description
        descriptions = {
            "AD": "El Alineamiento Dinámico garantiza que todas las unidades organizacionales, plantas y equipos compartan una visión digital coherente. En el caso Arçelik, la coordinación entre grupos de manufactura, IT, automatización, simulación y el socio startup fue el mecanismo que hizo posible el proyecto.",
            "LD": "El Liderazgo Digital implica desarrollar líderes que puedan navegar la incertidumbre tecnológica, tomar decisiones no convencionales y movilizar organizaciones hacia la transformación. En Arçelik, fue la apuesta por Simularge —en lugar de un vendor establecido— la decisión que definió el éxito.",
            "IC": "La Innovación Centrada en el Cliente conecta la transformación interna del proceso con el valor percibido por el usuario final. El digital twin no solo mejoró indicadores operativos: redujo defectos visibles en el refrigerador que afectaban directamente la satisfacción del cliente.",
            "AO": "La Agilidad Operativa permitió al equipo iterar sobre el modelo, revisar supuestos y adaptar el alcance sin perder el cronograma ni el presupuesto. La adopción de prácticas ágiles fue la respuesta correcta ante la alta incertidumbre tecnológica del proyecto.",
            "DD": "Las Decisiones Basadas en Datos transformaron un proceso opaco —gobernado por el juicio tácito de operadores— en un sistema con visibilidad en tiempo real, modelos predictivos y dashboards operativos. La calidad y latencia del dato son habilitadores críticos de todo el programa.",
            "EC": "Los Ecosistemas de Colaboración demuestran que las grandes empresas pueden superar sus límites internos conectándose con el talento externo. La triada Arçelik–Simularge–ITU Çekirdek es un modelo replicable de innovación abierta en manufactura industrial.",
        }
        st.info(descriptions.get(pcode, ""))

        # Gauges for overall OKR progress
        st.markdown('<div class="section-header">Progreso por Objetivo Estratégico</div>', unsafe_allow_html=True)
        gcols = st.columns(len(pdata["okrs"]))
        for i, okr in enumerate(pdata["okrs"]):
            avg_pct = np.mean([kr_progress(kr) for kr in okr["krs"]])
            with gcols[i]:
                st.plotly_chart(gauge(avg_pct, okr["id"], color), use_container_width=True)
                st.caption(f"**{okr['title']}**")

        # OKR cards with KR progress bars
        st.markdown('<div class="section-header">Detalle de Key Results</div>', unsafe_allow_html=True)

        # Bar chart — all KRs
        all_kr_labels = []
        all_kr_pcts   = []
        for okr in pdata["okrs"]:
            for kr in okr["krs"]:
                all_kr_labels.append(f"{kr['id']}\n{kr['label'][:45]}")
                all_kr_pcts.append(kr_progress(kr))

        fig_bars = go.Figure()
        bar_colors = [color if p >= 80 else ("#FFA726" if p >= 50 else "#EF5350") for p in all_kr_pcts]
        fig_bars.add_trace(go.Bar(
            x=all_kr_pcts, y=all_kr_labels, orientation='h',
            marker_color=bar_colors,
            text=[f"{p:.0f}%" for p in all_kr_pcts],
            textposition="outside",
        ))
        fig_bars.update_layout(
            title=f"Progreso de KRs — {pdata['title']}",
            xaxis=dict(range=[0, 115], title="% hacia meta", showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=10)),
            height=max(300, len(all_kr_labels) * 52 + 80),
            margin=dict(l=20, r=60, t=50, b=20),
            paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="Inter", size=11),
        )
        fig_bars.add_vline(x=80, line_dash="dash", line_color="#546e7a", opacity=0.5,
                            annotation_text="Meta mínima", annotation_position="top")
        st.plotly_chart(fig_bars, use_container_width=True)

        # OKR expandable detail
        for okr in pdata["okrs"]:
            with st.expander(f"📌 {okr['id']} — {okr['title']}", expanded=False):
                st.markdown(f"**Justificación estratégica:** {okr['justif']}")
                st.markdown(f"**¿Por qué medir este OKR?** {okr['why_measure']}")
                st.markdown("---")
                for kr in okr["krs"]:
                    pct = kr_progress(kr)
                    pcol = "#2E7D32" if pct >= 80 else ("#E65100" if pct >= 50 else "#B71C1C")
                    c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 1.2])
                    with c1:
                        st.markdown(f"**{kr['id']}** — {kr['label']}")
                        st.markdown(
                            f'<div class="progress-wrap"><div class="progress-fill" style="width:{pct}%;background:{pcol};"></div></div>',
                            unsafe_allow_html=True,
                        )
                    with c2:
                        st.metric("Actual", str(kr["current"]))
                    with c3:
                        st.metric("Meta", str(kr["target"]))
                    with c4:
                        st.metric("Progreso", f"{pct:.0f}%")
                    st.caption(f"Owner: **{kr['owner']}** · Cadencia: **{kr['cadencia']}**")
                    st.markdown("")

        # Trend simulation
        st.markdown('<div class="section-header">Simulación de Progreso — Proyección 12 Meses</div>', unsafe_allow_html=True)

        # Generate simulated projection
        trend_data = {}
        for okr in pdata["okrs"]:
            avg_now = np.mean([kr_progress(kr) for kr in okr["krs"]])
            projected = np.linspace(avg_now * 0.8, min(avg_now * 1.25, 98), 12)
            projected += np.random.normal(0, 1.5, 12)
            projected = np.clip(projected, 0, 100)
            trend_data[okr["id"]] = projected.tolist()

        color_map = {okr["id"]: c for okr, c in zip(pdata["okrs"],
                    [color, "#546e7a", "#90a4ae"])}
        fig_trend = line_trend(months, trend_data, f"Proyección de Progreso — {pdata['title']}", color_map)
        fig_trend.add_hline(y=80, line_dash="dot", line_color="#2E7D32", opacity=0.6,
                             annotation_text="Umbral mínimo 80%")
        st.plotly_chart(fig_trend, use_container_width=True)

        # KR owner table
        st.markdown('<div class="section-header">Tabla de Responsabilidades y Estado</div>', unsafe_allow_html=True)
        table_rows = []
        for okr in pdata["okrs"]:
            for kr in okr["krs"]:
                pct = kr_progress(kr)
                estado = "🟢 En meta" if pct >= 80 else ("🟡 En progreso" if pct >= 50 else "🔴 Crítico")
                table_rows.append({
                    "KR": kr["id"],
                    "Indicador": kr["label"],
                    "Actual": kr["current"],
                    "Meta": kr["target"],
                    "Progreso %": f"{pct:.0f}%",
                    "Owner": kr["owner"],
                    "Cadencia": kr["cadencia"],
                    "Estado": estado,
                })
        df_table = pd.DataFrame(table_rows)
        st.dataframe(df_table, use_container_width=True, hide_index=True,
                     column_config={"Progreso %": st.column_config.TextColumn("Progreso %")})
