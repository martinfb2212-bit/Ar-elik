"""
Dashboard Ejecutivo — Transformación Digital Arçelik
OKRs Estratégicos: 6 Pivotes de Capacidades Dinámicas
Estética inspirada en Rosaprima — lujo sutil, elegancia floral ecuatoriana
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arçelik · Digital Twin OKRs",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Rosaprima-inspired palette ────────────────────────────────────────────────
# Ivory white, warm cream, dusty rose, sage green, deep burgundy, warm charcoal
RP = {
    "ivory":      "#FAF7F2",      # page background
    "cream":      "#F2EDE4",      # card background
    "cream_dark": "#E8E0D4",      # borders, dividers
    "parchment":  "#EDE5D8",      # sidebar
    "rose_pale":  "#D4A5A0",      # accent rose (soft)
    "rose_deep":  "#9C4A52",      # primary accent (burgundy rose)
    "rose_mid":   "#B8706A",      # mid-tone rose
    "sage":       "#8A9E85",      # sage green accent
    "sage_light": "#C5D4C0",      # light sage
    "gold":       "#B8974A",      # warm gold for highlights
    "gold_light": "#D4B96A",      # light gold
    "charcoal":   "#2C2825",      # primary text
    "warm_gray":  "#7A726A",      # secondary text
    "light_gray": "#A89E94",      # placeholder / muted
    "white":      "#FFFFFF",
}

# ── Global CSS — Rosaprima aesthetic ─────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {{
    font-family: 'Jost', sans-serif;
    color: {RP['charcoal']};
  }}
  .stApp {{
    background-color: {RP['ivory']};
  }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{
    background-color: {RP['parchment']};
    border-right: 1px solid {RP['cream_dark']};
  }}
  section[data-testid="stSidebar"] * {{
    color: {RP['charcoal']} !important;
    font-family: 'Jost', sans-serif !important;
  }}
  section[data-testid="stSidebar"] .stRadio label {{
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    color: {RP['warm_gray']} !important;
    text-transform: uppercase;
  }}
  section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {RP['warm_gray']} !important;
  }}

  /* ── Typography ── */
  h1, h2, h3 {{
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 400;
    letter-spacing: 0.03em;
    color: {RP['charcoal']};
  }}

  /* ── Hero banner ── */
  .rp-hero {{
    background-color: {RP['charcoal']};
    background-image:
      linear-gradient(135deg, {RP['charcoal']} 0%, #3D2E2A 60%, {RP['rose_deep']} 100%);
    border-radius: 4px;
    padding: 44px 52px;
    color: {RP['ivory']};
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
  }}
  .rp-hero::before {{
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(212,165,160,0.08);
  }}
  .rp-hero::after {{
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(184,151,74,0.06);
  }}
  .rp-hero-eyebrow {{
    font-family: 'Jost', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {RP['rose_pale']};
    margin-bottom: 14px;
  }}
  .rp-hero h1 {{
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2.8rem;
    font-weight: 300;
    color: {RP['ivory']} !important;
    margin: 0 0 10px 0;
    line-height: 1.15;
    letter-spacing: 0.04em;
  }}
  .rp-hero p {{
    font-size: 0.88rem;
    color: rgba(250,247,242,0.65);
    margin: 0;
    letter-spacing: 0.05em;
    font-weight: 300;
  }}

  /* ── Section divider ── */
  .rp-divider {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 36px 0 20px 0;
  }}
  .rp-divider-line {{
    flex: 1;
    height: 1px;
    background: {RP['cream_dark']};
  }}
  .rp-divider-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    font-weight: 400;
    color: {RP['rose_deep']};
    letter-spacing: 0.1em;
    white-space: nowrap;
  }}
  .rp-divider-ornament {{
    font-size: 0.85rem;
    color: {RP['rose_pale']};
  }}

  /* ── Cards ── */
  .rp-card {{
    background: {RP['white']};
    border: 1px solid {RP['cream_dark']};
    border-radius: 3px;
    padding: 28px 32px;
    margin-bottom: 18px;
    position: relative;
  }}
  .rp-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: {RP['rose_pale']};
    border-radius: 3px 0 0 3px;
  }}
  .rp-card-title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 500;
    color: {RP['charcoal']};
    margin-bottom: 8px;
    letter-spacing: 0.03em;
  }}
  .rp-card-body {{
    font-size: 0.86rem;
    color: {RP['warm_gray']};
    line-height: 1.7;
    font-weight: 300;
  }}
  .rp-card-label {{
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {RP['rose_mid']};
    margin-bottom: 10px;
    font-weight: 500;
  }}

  /* ── Metric cards ── */
  .rp-metric {{
    background: {RP['white']};
    border: 1px solid {RP['cream_dark']};
    border-radius: 3px;
    padding: 24px 26px 20px 26px;
    text-align: center;
    margin-bottom: 12px;
  }}
  .rp-metric-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 500;
    color: {RP['charcoal']};
    line-height: 1.1;
  }}
  .rp-metric-label {{
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: {RP['light_gray']};
    margin-top: 6px;
    font-weight: 500;
  }}
  .rp-metric-delta {{
    font-size: 0.78rem;
    margin-top: 4px;
    color: {RP['sage']};
    font-weight: 400;
  }}

  /* ── Progress bar ── */
  .rp-progress-wrap {{
    background: {RP['cream']};
    border-radius: 2px;
    height: 5px;
    width: 100%;
    margin-top: 6px;
  }}
  .rp-progress-fill {{
    height: 5px;
    border-radius: 2px;
  }}

  /* ── Pivote badge ── */
  .rp-badge {{
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 500;
    color: {RP['rose_deep']};
    border: 1px solid {RP['rose_pale']};
    border-radius: 2px;
    padding: 3px 10px;
    margin-bottom: 18px;
    background: rgba(212,165,160,0.06);
  }}

  /* ── OKR expander ── */
  .streamlit-expanderHeader {{
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.05rem !important;
    font-weight: 400 !important;
    color: {RP['charcoal']} !important;
    letter-spacing: 0.04em !important;
    background: {RP['ivory']} !important;
    border: 1px solid {RP['cream_dark']} !important;
    border-radius: 3px !important;
  }}
  .streamlit-expanderContent {{
    background: {RP['white']} !important;
    border: 1px solid {RP['cream_dark']} !important;
    border-top: none !important;
  }}

  /* ── Table ── */
  .dataframe {{
    font-size: 0.82rem !important;
    font-family: 'Jost', sans-serif !important;
  }}

  /* ── Sidebar brand ── */
  .rp-sidebar-brand {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: {RP['charcoal']};
    letter-spacing: 0.1em;
    margin-bottom: 4px;
  }}
  .rp-sidebar-sub {{
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {RP['light_gray']};
    margin-bottom: 24px;
    font-weight: 400;
  }}
  .rp-sidebar-divider {{
    height: 1px;
    background: {RP['cream_dark']};
    margin: 16px 0;
  }}

  /* ── Info box override ── */
  .stAlert {{
    background-color: {RP['cream']} !important;
    border-color: {RP['cream_dark']} !important;
    border-radius: 3px !important;
    font-size: 0.86rem !important;
    color: {RP['warm_gray']} !important;
  }}
</style>
""", unsafe_allow_html=True)

# ── Palette for charts (warm, muted, elegant) ─────────────────────────────────
CHART_COLORS = {
    "AD": "#9C4A52",
    "LD": "#8A9E85",
    "IC": "#B8974A",
    "AO": "#B8706A",
    "DD": "#7A8EA0",
    "EC": "#8C7A6A",
}

# ── Data simulation ───────────────────────────────────────────────────────────
np.random.seed(42)
months = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
scrap_pre  = [6.8, 7.2, 6.1, 5.8, 6.3, 5.5, 2.1, 1.8, 1.5, 1.3, 1.1, 1.0]
oee_series = [70, 71, 69, 72, 71, 70, 82, 85, 87, 88, 89, 90]

# ── OKR dataset ───────────────────────────────────────────────────────────────
okr_data = {
    "AD": {
        "title": "Alineamiento Dinámico",
        "color": CHART_COLORS["AD"],
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
                    {"id": "KR-AD-03.2", "label": "Reducción tiempo aprobación (%)", "current": 28, "target": 40, "owner": "PMO Corp.", "cadencia": "Trimestral"},
                    {"id": "KR-AD-03.3", "label": "NPS interno equipos digitales", "current": 32, "target": 40, "owner": "Dir. RRHH", "cadencia": "Semestral"},
                ],
            },
        ],
    },
    "LD": {
        "title": "Liderazgo Digital",
        "color": CHART_COLORS["LD"],
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
                "justif": "Arçelik ya fue reconocido como Global Lighthouse Factory en Rumanía. El liderazgo digital externo refuerza la marca y atrae talento.",
                "why_measure": "El reconocimiento externo no es vanidad corporativa: es una señal que atrae talento, inversión y nuevas colaboraciones. Medir la presencia en rankings y la velocidad de cobertura de vacantes digitales permite evaluar si la reputación digital de Arçelik se está traduciendo en ventajas competitivas tangibles.",
                "krs": [
                    {"id": "KR-LD-02.1", "label": "Plantas certificadas WEF adicionales", "current": 0, "target": 2, "owner": "CEO / Dir. Estrategia", "cadencia": "Anual"},
                    {"id": "KR-LD-02.2", "label": "Publicaciones/presentaciones I4.0", "current": 4, "target": 6, "owner": "Dir. Comunicaciones", "cadencia": "Semestral"},
                    {"id": "KR-LD-02.3", "label": "Vacantes digitales cubiertas en 60 días (%)", "current": 68, "target": 80, "owner": "CPO", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-LD-03",
                "title": "Normalizar cultura de experimentación digital",
                "justif": "Arçelik intentó ML y FEA antes del digital twin. La capacidad de pivotar sin abandonar el proyecto debe institucionalizarse.",
                "why_measure": "Una cultura que no mide su propia capacidad de experimentar tiende a recaer en el conservadurismo. Cuantificar el número de experimentos lanzados, la velocidad de decisión en contextos de incertidumbre y el clima de innovación permite saber si la mentalidad ágil está arraigando o si fue un evento puntual.",
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
        "color": CHART_COLORS["IC"],
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
                    {"id": "KR-IC-03.3", "label": "Mejoras originadas en datos cliente", "current": 5, "target": 8, "owner": "Dir. Mejora Continua", "cadencia": "Trimestral"},
                ],
            },
        ],
    },
    "AO": {
        "title": "Agilidad Operativa",
        "color": CHART_COLORS["AO"],
        "okrs": [
            {
                "id": "OBJ-AO-01",
                "title": "Institucionalizar metodologías ágiles",
                "justif": "El modelo waterfall era inadecuado para alta incertidumbre tecnológica. La agilidad fue la decisión que salvó presupuesto y cronograma del proyecto.",
                "why_measure": "La adopción de metodologías ágiles declarada en un documento no equivale a capacidad organizacional real. Medir la velocidad de sprint, la desviación de presupuesto y la cobertura ágil permite determinar si la organización ha internalizado el método o si solo lo aplica superficialmente bajo presión.",
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
                "why_measure": "Un sistema de detección sin respuesta rápida no genera valor operativo. Medir la latencia desde la alerta hasta la corrección y el porcentaje de correcciones automáticas revela el nivel de madurez real del sistema. Es el indicador que separa un digital twin informativo de uno verdaderamente operativo.",
                "krs": [
                    {"id": "KR-AO-02.1", "label": "Tiempo alerta → corrección manual (min)", "current": 42, "target": 30, "owner": "Dir. Operaciones", "cadencia": "Mensual"},
                    {"id": "KR-AO-02.2", "label": "Correcciones automáticas / total (%)", "current": 48, "target": 70, "owner": "Dir. Automatización", "cadencia": "Trimestral"},
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
        "color": CHART_COLORS["DD"],
        "okrs": [
            {
                "id": "OBJ-DD-01",
                "title": "Construir infraestructura de datos robusta",
                "justif": "Sin la infraestructura PLC/IoT existente, el digital twin no habría sido posible. Formalizar y escalar esta infraestructura es prerequisito para decisiones basadas en datos.",
                "why_measure": "Una decisión basada en datos de mala calidad o con alta latencia puede ser más dañina que una decisión intuitiva. Medir la cobertura de sensores, el uptime del pipeline y la latencia de datos asegura que el digital twin opere sobre información confiable. Sin estas métricas, la precisión del modelo es una incógnita.",
                "krs": [
                    {"id": "KR-DD-01.1", "label": "Parámetros críticos monitoreados RT (%)", "current": 81, "target": 95, "owner": "Dir. IT", "cadencia": "Trimestral"},
                    {"id": "KR-DD-01.2", "label": "Uptime infraestructura de datos (%)", "current": 98.7, "target": 99.5, "owner": "CTO", "cadencia": "Mensual"},
                    {"id": "KR-DD-01.3", "label": "Latencia captura → dashboard (seg)", "current": 18, "target": 10, "owner": "Dir. IT / Arquitectura", "cadencia": "Mensual"},
                ],
            },
            {
                "id": "OBJ-DD-02",
                "title": "Transformar conocimiento tácito en modelos explícitos",
                "justif": "El conocimiento tácito de operadores era el principal activo no codificado del proceso. Digitalizarlo fue una de las contribuciones más importantes del proyecto.",
                "why_measure": "El conocimiento tácito no medido es un riesgo de continuidad operativa: si un operador experto se va, el conocimiento se va con él. Medir qué porcentaje del saber-hacer ha sido codificado permite gestionar este riesgo y cuantificar el avance real de la digitalización del capital intelectual.",
                "krs": [
                    {"id": "KR-DD-02.1", "label": "Procedimientos críticos codificados en DT (%)", "current": 55, "target": 80, "owner": "Dir. Ing. Proceso", "cadencia": "Trimestral"},
                    {"id": "KR-DD-02.2", "label": "MAPE del digital twin vs. valores reales", "current": 7.2, "target": 5.0, "owner": "Eq. Simulación", "cadencia": "Mensual"},
                    {"id": "KR-DD-02.3", "label": "Ajustes guiados por sistema (%)", "current": 48, "target": 65, "owner": "Dir. Operaciones", "cadencia": "Trimestral"},
                ],
            },
            {
                "id": "OBJ-DD-03",
                "title": "Desarrollar capacidades de analytics avanzado",
                "justif": "El intento inicial de ML falló por limitaciones en feature engineering. Internalizar esta capacidad es crítico para la autonomía analítica de Arçelik.",
                "why_measure": "Depender de Simularge para todo el feature engineering crea una vulnerabilidad estratégica. Medir los data scientists internos certificados, las iteraciones de mejora del modelo y el porcentaje de detección predictiva permite evaluar si Arçelik está construyendo soberanía analítica o perpetuando la dependencia externa.",
                "krs": [
                    {"id": "KR-DD-03.1", "label": "Data scientists certificados internos", "current": 11, "target": 20, "owner": "CPO / CTO", "cadencia": "Semestral"},
                    {"id": "KR-DD-03.2", "label": "Iteraciones mejora de modelo / año / planta", "current": 2, "target": 4, "owner": "Dir. R&D", "cadencia": "Trimestral"},
                    {"id": "KR-DD-03.3", "label": "Defectos detectados predictivamente (%)", "current": 52, "target": 75, "owner": "Dir. Calidad / Analytics", "cadencia": "Mensual"},
                ],
            },
        ],
    },
    "EC": {
        "title": "Ecosistemas de Colaboración",
        "color": CHART_COLORS["EC"],
        "okrs": [
            {
                "id": "OBJ-EC-01",
                "title": "Fortalecer ecosistema startup–academia–empresa",
                "justif": "La conexión con ITU Çekirdek y Simularge fue más efectiva que contratar a un vendor establecido. Este modelo debe convertirse en capacidad sistemática.",
                "why_measure": "Sin métricas, el ecosistema de colaboración queda como un logro puntual. Medir el número de startups activas, los proyectos co-desarrollados y el ROI comparativo permite demostrar al consejo que la apuesta por el ecosistema genera más valor que el modelo transaccional tradicional.",
                "krs": [
                    {"id": "KR-EC-01.1", "label": "Startups activas en proyectos colaborativos", "current": 7, "target": 15, "owner": "Dir. Atölye 4.0", "cadencia": "Trimestral"},
                    {"id": "KR-EC-01.2", "label": "Proyectos co-desarrollados con universidades", "current": 4, "target": 8, "owner": "Dir. R&D", "cadencia": "Trimestral"},
                    {"id": "KR-EC-01.3", "label": "ROI proyectos con startups vs. internos (x)", "current": 1.3, "target": 1.5, "owner": "CFO / Dir. Innovación", "cadencia": "Anual"},
                ],
            },
            {
                "id": "OBJ-EC-02",
                "title": "Desarrollar modelo replicable empresa–startup",
                "justif": "Arçelik tenía reglas estrictas y procedimientos rígidos para colaborar con startups. Reducir estas fricciones es una capacidad organizacional estratégica.",
                "why_measure": "La fricción en el proceso de onboarding de startups no solo ralentiza proyectos: disuade al mejor talento emprendedor. Medir el tiempo de negociación, la adopción del playbook y la satisfacción de los socios permite cuantificar si la organización está volviéndose genuinamente colaborativa o solo aparentándolo.",
                "krs": [
                    {"id": "KR-EC-02.1", "label": "Tiempo contacto → acuerdo startup (días)", "current": 68, "target": 45, "owner": "Dir. Legal / PMO", "cadencia": "Por proyecto"},
                    {"id": "KR-EC-02.2", "label": "Proyectos con playbook estandarizado (%)", "current": 55, "target": 100, "owner": "Dir. Atölye 4.0", "cadencia": "Trimestral"},
                    {"id": "KR-EC-02.3", "label": "Satisfacción startups socios (1–10)", "current": 7.2, "target": 8.0, "owner": "Dir. Atölye 4.0", "cadencia": "Anual"},
                ],
            },
            {
                "id": "OBJ-EC-03",
                "title": "Posicionar Arçelik como hub de innovación manufacturera",
                "justif": "La relación con ITU Çekirdek y el reconocimiento Global Lighthouse posiciona a Arçelik como polo gravitacional del ecosistema.",
                "why_measure": "El posicionamiento como hub de innovación no es un objetivo de relaciones públicas: es una palanca de acceso a co-financiamiento, talento de élite y nuevas colaboraciones. Medir el porcentaje de proyectos con financiamiento externo y la presencia en rankings permite evaluar el retorno estratégico de esta inversión de reputación.",
                "krs": [
                    {"id": "KR-EC-03.1", "label": "Proyectos con co-financiamiento externo (%)", "current": 18, "target": 30, "owner": "Dir. R&D / CFO", "cadencia": "Anual"},
                    {"id": "KR-EC-03.2", "label": "Startups escaladas con apoyo Arçelik", "current": 2, "target": 5, "owner": "Dir. Atölye 4.0", "cadencia": "Anual"},
                    {"id": "KR-EC-03.3", "label": "Rankings internacionales como caso I4.0", "current": 1, "target": 3, "owner": "CEO / Dir. Estrategia", "cadencia": "Anual"},
                ],
            },
        ],
    },
}

PIVOTES = {
    "Alineamiento Dinámico":        "AD",
    "Liderazgo Digital":             "LD",
    "Innovación Centrada al Cliente":"IC",
    "Agilidad Operativa":            "AO",
    "Decisiones Basadas en Datos":   "DD",
    "Ecosistemas de Colaboración":   "EC",
}

# ── Helper: compute KR progress 0–100 ────────────────────────────────────────
def kr_progress(kr):
    c, t = kr["current"], kr["target"]
    lbl = kr["label"].lower()
    lower_better = any(k in lbl for k in ["tiempo","latencia","mape","scrap","días","días"])
    if lower_better:
        baseline = max(c * 1.5, t * 2)
        pct = (baseline - c) / (baseline - t) * 100
    else:
        pct = c / t * 100
    return round(min(max(pct, 0), 100), 1)

def progress_color(pct):
    if pct >= 80: return RP["sage"]
    if pct >= 50: return RP["gold"]
    return RP["rose_mid"]

# ── Chart helpers ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor=RP["white"],
    plot_bgcolor=RP["white"],
    font=dict(family="Jost, sans-serif", color=RP["charcoal"], size=12),
    margin=dict(l=12, r=12, t=48, b=16),
)

def gauge_rp(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 26, "family": "Cormorant Garamond, serif", "color": RP["charcoal"]}},
        title={"text": title, "font": {"size": 12, "family": "Jost, sans-serif", "color": RP["warm_gray"]}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 9}, "tickcolor": RP["light_gray"],
                     "tickwidth": 1, "linecolor": RP["cream_dark"]},
            "bar": {"color": color, "thickness": 0.55},
            "bgcolor": RP["cream"],
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50],  "color": "#FAF0EE"},
                {"range": [50, 80], "color": "#FAF5EA"},
                {"range": [80, 100],"color": "#EFF5EE"},
            ],
            "threshold": {"line": {"color": RP["charcoal"], "width": 2}, "thickness": 0.7, "value": 80},
        }
    ))
    fig.update_layout(height=200, **PLOTLY_LAYOUT)
    return fig

def radar_rp(codes, names, vals):
    vals_c = vals + [vals[0]]
    names_c = names + [names[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_c, theta=names_c, fill="toself",
        fillcolor=f"rgba(156,74,82,0.10)",
        line=dict(color=RP["rose_deep"], width=1.5),
        name="Progreso",
    ))
    fig.add_trace(go.Scatterpolar(
        r=[80]*len(names_c), theta=names_c,
        line=dict(color=RP["sage_light"], width=1, dash="dot"),
        mode="lines", name="Umbral 80%",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color=RP["light_gray"]),
                            gridcolor=RP["cream_dark"], linecolor=RP["cream_dark"]),
            angularaxis=dict(tickfont=dict(size=11, family="Cormorant Garamond, serif"), gridcolor=RP["cream_dark"]),
            bgcolor=RP["white"],
        ),
        showlegend=True,
        height=400,
        legend=dict(font=dict(size=11), bgcolor=RP["white"]),
        title=dict(text="Progreso Global por Pivote Estratégico",
                   font=dict(family="Cormorant Garamond, serif", size=18, color=RP["charcoal"])),
        **PLOTLY_LAYOUT,
    )
    return fig

def bar_rp(labels, pcts, color, title):
    bar_colors = [color if p >= 80 else (RP["gold"] if p >= 50 else RP["rose_mid"]) for p in pcts]
    fig = go.Figure(go.Bar(
        x=pcts, y=labels, orientation="h",
        marker_color=bar_colors, marker_line_width=0,
        text=[f"{p:.0f}%" for p in pcts], textposition="outside",
        textfont=dict(size=11, color=RP["warm_gray"]),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    fig.add_vline(x=80, line_dash="dot", line_color=RP["cream_dark"],
                  annotation_text="Meta mínima",
                  annotation_font=dict(size=10, color=RP["light_gray"]))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Cormorant Garamond, serif", size=17, color=RP["charcoal"])),
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, tickfont=dict(color=RP["light_gray"])),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color=RP["warm_gray"])),
        height=max(260, len(labels) * 52 + 80),
        **PLOTLY_LAYOUT,
    )
    return fig

def line_rp(months, series, color, title):
    fig = go.Figure()
    colors = [color, RP["gold"], RP["sage"]]
    for i, (name, vals) in enumerate(series.items()):
        fig.add_trace(go.Scatter(
            x=months, y=vals, mode="lines+markers", name=name,
            line=dict(color=colors[i % len(colors)], width=1.8),
            marker=dict(size=5, color=colors[i % len(colors)]),
        ))
    fig.add_hline(y=80, line_dash="dot", line_color=RP["cream_dark"],
                  annotation_text="Umbral 80%", annotation_font=dict(size=10, color=RP["light_gray"]))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Cormorant Garamond, serif", size=17, color=RP["charcoal"])),
        xaxis=dict(showgrid=False, tickfont=dict(color=RP["light_gray"])),
        yaxis=dict(showgrid=True, gridcolor=RP["cream"], tickfont=dict(color=RP["light_gray"])),
        legend=dict(font=dict(size=11), bgcolor=RP["white"], bordercolor=RP["cream_dark"], borderwidth=1),
        height=280,
        **PLOTLY_LAYOUT,
    )
    return fig

def divider(text):
    st.markdown(f"""
    <div class="rp-divider">
      <div class="rp-divider-line"></div>
      <span class="rp-divider-text">{text}</span>
      <div class="rp-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="rp-sidebar-brand">Arçelik</div>
    <div class="rp-sidebar-sub">Digital Twin · OKRs Estratégicos</div>
    <div class="rp-sidebar-divider"></div>
    """, unsafe_allow_html=True)

    pages = ["Ambiente del Problema", "Resumen Ejecutivo"] + list(PIVOTES.keys())
    page = st.radio("", pages, label_visibility="collapsed")

    st.markdown(f'<div class="rp-sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <p style="font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;
    color:{RP['light_gray']};line-height:1.8;font-weight:400;">
    Caso · Arçelik × Simularge<br>
    Curso · Evolución Digital<br>
    Capacidades Dinámicas<br>
    Año · 2024
    </p>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — AMBIENTE DEL PROBLEMA
# ══════════════════════════════════════════════════════════════════════════════
if page == "Ambiente del Problema":

    st.markdown(f"""
    <div class="rp-hero">
      <div class="rp-hero-eyebrow">Evolución Digital · Capacidades Dinámicas</div>
      <h1>Digitalización del Proceso<br>de Termoformado</h1>
      <p>Arçelik × Simularge · Istanbul, Turquía · Caso de Transformación Industrial</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("$2 M+", "Ahorro Anual Inicial", "↑ Año 1 post-implementación"),
        ("1,600 t", "Plástico Ahorrado", "↑ por año"),
        ("5–8% → 1–2%", "Scrap Ratio", "↓ Reducción significativa"),
        ("68% → 90%", "OEE Máximo", "↑ Eficiencia global"),
    ]
    for col, (val, lbl, delta) in zip([c1,c2,c3,c4], metrics):
        with col:
            st.markdown(f"""
            <div class="rp-metric">
              <div class="rp-metric-value">{val}</div>
              <div class="rp-metric-label">{lbl}</div>
              <div class="rp-metric-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    divider("Ambiente del Problema")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown(f"""
        <div class="rp-card">
          <div class="rp-card-label">Tomador de Decisiones</div>
          <div class="rp-card-title">Dirección de Tecnologías de Producción — Arçelik A.Ş.</div>
          <div class="rp-card-body">
            Equipo liderado por la Dirección de Manufactura y el Centro de Competencias
            <em>Atölye 4.0</em>, con participación de los grupos de manufactura inteligente,
            producción, ingeniería y tecnologías de proceso y materiales.<br><br>
            Arçelik es el tercer fabricante de electrodomésticos más grande de Europa, con
            30,000 empleados, 12 marcas y 23 plantas en el mundo. El desafío fue liderado
            desde su unidad de innovación industrial fundada en 2016.
          </div>
        </div>
        <div class="rp-card">
          <div class="rp-card-label">Tarea Estratégica</div>
          <div class="rp-card-title">Desarrollar e implementar un gemelo digital del proceso de termoformado</div>
          <div class="rp-card-body">
            <strong style="color:{RP['charcoal']};font-weight:500;">Decisión central:</strong>
            Reducir consumo de plástico, disminuir el índice de desperdicio y mejorar la
            calidad del cuerpo interior del refrigerador mediante un digital twin en tiempo real.<br><br>
            <strong style="color:{RP['charcoal']};font-weight:500;">Transformación requerida:</strong><br>
            · Digitalizar un proceso gobernado por conocimiento tácito de operadores.<br>
            · Elegir entre vendor establecido vs. colaboración con startup especializada.<br>
            · Adoptar metodologías ágiles en una organización con estructuras rígidas.<br>
            · Diseñar un modelo de despliegue global desde un piloto de una sola planta.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div class="rp-card" style="height:100%;">
          <div class="rp-card-label">Entorno Estratégico</div>
          <div class="rp-card-title">Factores que condicionan la decisión</div>
          <div class="rp-card-body">
            <strong style="color:{RP['charcoal']};font-weight:500;">Industria</strong><br>
            Manufactura de bienes duraderos. Presión constante sobre costos, calidad y
            sostenibilidad. Arçelik compite en 150+ países bajo 12 marcas.<br><br>
            <strong style="color:{RP['charcoal']};font-weight:500;">Cambio tecnológico</strong><br>
            Emergencia del paradigma Industria 4.0. Gartner proyectaba que el 50% de
            las empresas industriales adoptarían digital twins para 2021.<br><br>
            <strong style="color:{RP['charcoal']};font-weight:500;">Mercado</strong><br>
            Producción anual de ~20 millones de unidades. Los refrigeradores representan
            el 35% de la producción. El termoformado consume más de 20,000 toneladas
            de plástico por año — palanca de costo y sostenibilidad crítica.<br><br>
            <strong style="color:{RP['charcoal']};font-weight:500;">Regulatorio / Ambiental</strong><br>
            Inclusión en el Dow Jones Sustainability Index desde 2017. Premio Cero
            Residuos del Ministerio de Medio Ambiente de Turquía 2019. Alineamiento
            con ODS 12 de Naciones Unidas.<br><br>
            <strong style="color:{RP['charcoal']};font-weight:500;">Cultura organizacional</strong><br>
            Tensión entre la inercia estructural (procesos rígidos, aprobaciones múltiples)
            y la necesidad de agilidad para proyectos de alta incertidumbre tecnológica.
          </div>
        </div>
        """, unsafe_allow_html=True)

    divider("Línea de Tiempo")
    tl = pd.DataFrame({
        "Hito": ["Fundación Arçelik","Establecimiento Atölye 4.0","Fundación Simularge en ITU",
                  "Inicio Proyecto DT","Lighthouse Factory (WEF)","Implementación DT Piloto",
                  "Ahorro $2M+ confirmado","Plan Despliegue Global"],
        "Año":  [1955,2016,2017,2019,2019,2020,2020,2021],
        "Tipo": ["Empresa","Innovación","Ecosistema","Proyecto",
                  "Reconocimiento","Proyecto","Resultado","Estrategia"],
    })
    cmap = {"Empresa": RP["charcoal"], "Innovación": RP["rose_deep"], "Ecosistema": RP["sage"],
             "Proyecto": RP["gold"], "Reconocimiento": RP["sage"], "Resultado": RP["rose_mid"],
             "Estrategia": RP["warm_gray"]}
    fig_tl = px.scatter(tl, x="Año", y="Hito", color="Tipo", color_discrete_map=cmap, size_max=14)
    fig_tl.update_traces(marker=dict(size=14, line=dict(width=0)))
    fig_tl.update_layout(
        height=300,
        title=dict(text="", font=dict(size=16)),
        xaxis=dict(showgrid=True, gridcolor=RP["cream"], tickfont=dict(color=RP["light_gray"])),
        yaxis=dict(showgrid=False, tickfont=dict(size=10.5, color=RP["warm_gray"])),
        legend=dict(font=dict(size=11), bgcolor=RP["white"], bordercolor=RP["cream_dark"], borderwidth=1),
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_tl, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RESUMEN EJECUTIVO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resumen Ejecutivo":

    st.markdown(f"""
    <div class="rp-hero">
      <div class="rp-hero-eyebrow">Vista Consolidada</div>
      <h1>Resumen Ejecutivo</h1>
      <p>6 Pivotes Estratégicos · 18 Objetivos · 54 Key Results</p>
    </div>
    """, unsafe_allow_html=True)

    # Compute pivote scores
    scores = {}
    for code, data in okr_data.items():
        pcts = [kr_progress(kr) for okr in data["okrs"] for kr in okr["krs"]]
        scores[code] = round(np.mean(pcts), 1)

    # Radar + scores
    col_r1, col_r2 = st.columns([1.3, 1])
    with col_r1:
        codes = list(scores.keys())
        names = [okr_data[c]["title"] for c in codes]
        vals  = [scores[c] for c in codes]
        st.plotly_chart(radar_rp(codes, names, vals), use_container_width=True)

    with col_r2:
        divider("Estado por Pivote")
        for code, score in scores.items():
            col = progress_color(score)
            status = "En meta" if score >= 80 else ("En progreso" if score >= 50 else "Crítico")
            dot = "●" if score >= 80 else "●"
            st.markdown(f"""
            <div style="margin-bottom:16px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
                <span style="font-family:'Cormorant Garamond',serif;font-size:0.95rem;color:{RP['charcoal']};">
                  {okr_data[code]['title']}
                </span>
                <span style="font-size:0.75rem;color:{col};letter-spacing:0.1em;font-weight:500;">
                  {score}% &nbsp;·&nbsp; {status}
                </span>
              </div>
              <div class="rp-progress-wrap">
                <div class="rp-progress-fill" style="width:{score}%;background:{col};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Operational results
    divider("Resultados Operativos Clave")
    c1, c2 = st.columns(2)
    with c1:
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=months, y=scrap_pre, mode="lines+markers",
                                    line=dict(color=RP["rose_mid"], width=2),
                                    marker=dict(size=5), fill="tozeroy",
                                    fillcolor="rgba(184,112,106,0.08)", name="Scrap Ratio (%)"))
        fig_s.add_hline(y=2, line_dash="dot", line_color=RP["sage"],
                         annotation_text="Meta ≤2%", annotation_font=dict(size=10, color=RP["sage"]))
        fig_s.update_layout(title=dict(text="Scrap Ratio — Termoformado",
                                        font=dict(family="Cormorant Garamond, serif", size=17, color=RP["charcoal"])),
                             xaxis=dict(showgrid=False, tickfont=dict(color=RP["light_gray"])),
                             yaxis=dict(showgrid=True, gridcolor=RP["cream"], tickfont=dict(color=RP["light_gray"])),
                             height=260, **PLOTLY_LAYOUT)
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        fig_o = go.Figure()
        fig_o.add_trace(go.Scatter(x=months, y=oee_series, mode="lines+markers",
                                    line=dict(color=RP["sage"], width=2),
                                    marker=dict(size=5), fill="tozeroy",
                                    fillcolor="rgba(138,158,133,0.08)", name="OEE (%)"))
        fig_o.add_hline(y=82, line_dash="dot", line_color=RP["rose_mid"],
                         annotation_text="Meta ≥82%", annotation_font=dict(size=10, color=RP["rose_mid"]))
        fig_o.update_layout(title=dict(text="OEE — Eficiencia Global de Equipos",
                                        font=dict(family="Cormorant Garamond, serif", size=17, color=RP["charcoal"])),
                             xaxis=dict(showgrid=False, tickfont=dict(color=RP["light_gray"])),
                             yaxis=dict(showgrid=True, gridcolor=RP["cream"], tickfont=dict(color=RP["light_gray"])),
                             height=260, **PLOTLY_LAYOUT)
        st.plotly_chart(fig_o, use_container_width=True)

    # Heatmap
    divider("Mapa de Calor · 54 Key Results")
    rows = []
    for code, data in okr_data.items():
        for okr in data["okrs"]:
            for kr in okr["krs"]:
                rows.append({"Pivote": data["title"][:22], "KR": kr["id"], "Progreso": kr_progress(kr)})
    df_h = pd.DataFrame(rows)
    pivot_h = df_h.pivot(index="KR", columns="Pivote", values="Progreso").fillna(0)
    fig_h = px.imshow(pivot_h,
                       color_continuous_scale=[
                           [0.0, "#FAE8E6"], [0.5, "#F5EDD6"], [0.8, "#EBF2E8"], [1.0, RP["sage"]]
                       ],
                       zmin=0, zmax=100, aspect="auto")
    fig_h.update_layout(
        title=dict(text="Progreso (%) de cada KR por Pivote Estratégico",
                   font=dict(family="Cormorant Garamond, serif", size=17, color=RP["charcoal"])),
        height=580,
        coloraxis_colorbar=dict(title="% Progreso", tickfont=dict(size=10, color=RP["warm_gray"])),
        xaxis=dict(tickfont=dict(size=10, color=RP["warm_gray"])),
        yaxis=dict(tickfont=dict(size=9, color=RP["warm_gray"])),
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig_h, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PIVOTE PAGES
# ══════════════════════════════════════════════════════════════════════════════
else:
    pcode = PIVOTES.get(page)
    if pcode and pcode in okr_data:
        pdata = okr_data[pcode]
        color = pdata["color"]

        descriptions = {
            "AD": "El Alineamiento Dinámico garantiza que todas las unidades organizacionales compartan una visión digital coherente. En el caso Arçelik, la coordinación entre manufactura, IT, automatización y el startup Simularge fue el mecanismo que hizo posible el proyecto.",
            "LD": "El Liderazgo Digital implica desarrollar líderes que naveguen la incertidumbre tecnológica, tomen decisiones no convencionales y movilicen organizaciones hacia la transformación. En Arçelik, apostar por Simularge en lugar de un vendor establecido fue la decisión que definió el éxito.",
            "IC": "La Innovación Centrada en el Cliente conecta la transformación interna del proceso con el valor percibido por el usuario final. El digital twin no solo mejoró indicadores operativos: redujo defectos visibles en el refrigerador que afectaban directamente la satisfacción del cliente.",
            "AO": "La Agilidad Operativa permitió al equipo iterar sobre el modelo, revisar supuestos y adaptar el alcance sin perder el cronograma ni el presupuesto. La adopción de prácticas ágiles fue la respuesta correcta ante la alta incertidumbre tecnológica del proyecto.",
            "DD": "Las Decisiones Basadas en Datos transformaron un proceso opaco —gobernado por el juicio tácito de operadores— en un sistema con visibilidad en tiempo real, modelos predictivos y dashboards operativos.",
            "EC": "Los Ecosistemas de Colaboración demuestran que las grandes empresas pueden superar sus límites internos conectándose con el talento externo. La triada Arçelik–Simularge–ITU Çekirdek es un modelo replicable de innovación abierta en manufactura industrial.",
        }

        st.markdown(f"""
        <div class="rp-hero" style="background:linear-gradient(135deg,{RP['charcoal']} 0%,{color} 100%);">
          <div class="rp-hero-eyebrow">Pivote Estratégico</div>
          <h1>{page}</h1>
          <p>{len(pdata['okrs'])} Objetivos · {len(pdata['okrs'])*3} Key Results</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rp-card">
          <div class="rp-card-label">Descripción del Pivote</div>
          <div class="rp-card-body">{descriptions[pcode]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Gauges
        divider("Progreso por Objetivo")
        gcols = st.columns(len(pdata["okrs"]))
        for i, okr in enumerate(pdata["okrs"]):
            avg = np.mean([kr_progress(kr) for kr in okr["krs"]])
            with gcols[i]:
                st.plotly_chart(gauge_rp(avg, okr["id"], color), use_container_width=True)
                st.markdown(f"<p style='text-align:center;font-size:0.8rem;color:{RP['warm_gray']};font-family:Cormorant Garamond,serif;'>{okr['title']}</p>",
                            unsafe_allow_html=True)

        # Bar chart all KRs
        divider("Detalle de Key Results")
        labels, pcts = [], []
        for okr in pdata["okrs"]:
            for kr in okr["krs"]:
                labels.append(f"{kr['id']}  ·  {kr['label'][:48]}")
                pcts.append(kr_progress(kr))
        st.plotly_chart(bar_rp(labels, pcts, color, f"Progreso de KRs — {pdata['title']}"), use_container_width=True)

        # OKR expanders
        divider("Objetivos y Justificación")
        for okr in pdata["okrs"]:
            with st.expander(f"{okr['id']}  ·  {okr['title']}"):
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <span style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:{RP['rose_mid']};font-weight:500;">Justificación Estratégica</span>
                  <p style="font-size:0.86rem;color:{RP['warm_gray']};line-height:1.7;margin-top:4px;">
                  {okr['justif']}</p>
                </div>
                <div style="background:{RP['cream']};border-radius:3px;padding:16px 20px;margin-bottom:16px;
                border-left:3px solid {color};">
                  <span style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:{color};font-weight:500;">¿Por qué medir este OKR?</span>
                  <p style="font-size:0.86rem;color:{RP['charcoal']};line-height:1.7;margin-top:4px;">
                  {okr['why_measure']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<span style='font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:{RP['rose_mid']};font-weight:500;'>Key Results</span>", unsafe_allow_html=True)
                for kr in okr["krs"]:
                    pct = kr_progress(kr)
                    pcol = progress_color(pct)
                    status = "En meta" if pct >= 80 else ("En progreso" if pct >= 50 else "Crítico")
                    c1, c2, c3, c4 = st.columns([3.5, 1, 1, 1.2])
                    with c1:
                        st.markdown(f"<p style='font-size:0.87rem;color:{RP['charcoal']};margin-bottom:2px;'><strong>{kr['id']}</strong> — {kr['label']}</p>", unsafe_allow_html=True)
                        st.markdown(f'<div class="rp-progress-wrap"><div class="rp-progress-fill" style="width:{pct}%;background:{pcol};"></div></div>', unsafe_allow_html=True)
                    with c2:
                        st.metric("Actual", str(kr["current"]))
                    with c3:
                        st.metric("Meta", str(kr["target"]))
                    with c4:
                        st.metric("Progreso", f"{pct:.0f}%  {status}")
                    st.markdown(f"<p style='font-size:0.75rem;color:{RP['light_gray']};margin:0 0 10px 0;'>Owner: <strong>{kr['owner']}</strong> · Cadencia: {kr['cadencia']}</p>", unsafe_allow_html=True)

        # Trend projection
        divider("Proyección de Progreso · 12 Meses")
        trend = {}
        for okr in pdata["okrs"]:
            avg_now = np.mean([kr_progress(kr) for kr in okr["krs"]])
            projected = np.linspace(avg_now * 0.82, min(avg_now * 1.22, 97), 12)
            projected += np.random.normal(0, 1.2, 12)
            trend[okr["id"]] = np.clip(projected, 0, 100).tolist()
        st.plotly_chart(line_rp(months, trend, color, f"Proyección de Progreso — {pdata['title']}"), use_container_width=True)

        # Responsibility table
        divider("Tabla de Responsabilidades")
        rows = []
        for okr in pdata["okrs"]:
            for kr in okr["krs"]:
                pct = kr_progress(kr)
                estado = "✦ En meta" if pct >= 80 else ("◆ En progreso" if pct >= 50 else "◇ Crítico")
                rows.append({
                    "KR": kr["id"], "Indicador": kr["label"],
                    "Actual": kr["current"], "Meta": kr["target"],
                    "Progreso": f"{pct:.0f}%",
                    "Owner": kr["owner"], "Cadencia": kr["cadencia"], "Estado": estado,
                })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
