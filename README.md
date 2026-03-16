# 🏭 Arçelik Digital Twin — Dashboard Ejecutivo OKRs

> **Curso:** Evolución Digital y Orquestación de Capacidades Dinámicas  
> **Caso:** Arçelik × Simularge — Digitalización del Proceso de Termoformado  
> **Framework:** 6 Pivotes Estratégicos · 18 Objetivos · 54 Key Results

---

## 📋 Descripción del Caso

Arçelik, tercer fabricante de electrodomésticos más grande de Europa (30,000 empleados, 23 plantas, 12 marcas), desarrolló un **gemelo digital (digital twin)** de su proceso de termoformado en colaboración con **Simularge**, un startup de Estambul especializado en simulación industrial.

El proceso de termoformado —usado para fabricar el cuerpo interior de los refrigeradores— consume más de **20,000 toneladas de plástico/año** y representaba un cuello de botella de calidad y sostenibilidad. El proyecto resultó en:

| Métrica | Antes | Después |
|---|---|---|
| Scrap ratio | 5–8% | 1–2% |
| OEE | 68–75% | 82–92% |
| Ahorro materiales | — | $2M+/año |
| Plástico ahorrado | — | 1,600 t/año |

---

## 🔑 Los 6 Pivotes Estratégicos

| # | Pivote | Descripción |
|---|---|---|
| 1 | **Alineamiento Dinámico** | Visión digital compartida entre unidades de manufactura, IT, automatización y socios externos |
| 2 | **Liderazgo Digital** | Líderes capaces de navegar incertidumbre tecnológica y colaborar con startups |
| 3 | **Innovación Centrada en el Cliente** | Reducción de defectos visibles y aceleración del time-to-market de nuevos modelos |
| 4 | **Agilidad Operativa** | Metodologías ágiles y control adaptativo en tiempo real del proceso |
| 5 | **Decisiones Basadas en Datos** | Transformación del conocimiento tácito en modelos explícitos con IoT + FEM |
| 6 | **Ecosistemas de Colaboración** | Modelo Arçelik–Simularge–ITU Çekirdek como referente de innovación abierta |

---

## 🚀 Cómo Ejecutar

### Requisitos previos
- Python 3.9 o superior
- pip

### Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/arcelik-digital-twin-okrs.git
cd arcelik-digital-twin-okrs

# 2. (Recomendado) Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el dashboard
streamlit run app.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

---

## 📁 Arquitectura del Proyecto

```
arcelik-digital-twin-okrs/
│
├── app.py              # Dashboard completo (Streamlit)
│   ├── Página 1        # Ambiente del Problema
│   ├── Página 2        # Resumen Ejecutivo (radar + heatmap)
│   └── Páginas 3–8     # Un pivote por página (OKRs + KRs + gauges + tendencias)
│
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

> ⚠️ **Sin archivos de datos externos.** Toda la simulación de datos está integrada directamente en `app.py`.

---

## 🖥️ Páginas del Dashboard

| Página | Contenido |
|---|---|
| 🏠 Ambiente del Problema | Tomador de decisiones, tarea estratégica, entorno, KPIs iniciales, línea de tiempo |
| 📊 Resumen Ejecutivo | Radar de 6 pivotes, heatmap de 54 KRs, evolución de scrap y OEE |
| 🔗 Alineamiento Dinámico | 3 OKRs, 9 KRs, gauges, barras de progreso, proyección, tabla de responsabilidades |
| 💡 Liderazgo Digital | Idem — enfoque en certificaciones, cultura de innovación, reconocimiento externo |
| 👤 Innovación al Cliente | Idem — enfoque en calidad, time-to-market, integración de datos de campo |
| ⚡ Agilidad Operativa | Idem — enfoque en metodologías ágiles, respuesta correctiva, optimización de materiales |
| 📊 Decisiones por Datos | Idem — enfoque en infraestructura IoT, codificación de conocimiento tácito, predictividad |
| 🤝 Ecosistemas de Colab. | Idem — enfoque en startups activos, modelo empresa-startup, posicionamiento global |

---

## 🛠️ Stack Tecnológico

| Librería | Uso |
|---|---|
| `streamlit` | Framework del dashboard |
| `pandas` | Manipulación de datos |
| `plotly` | Visualizaciones interactivas (gauges, radar, barras, heatmap, líneas) |
| `numpy` | Simulación de datos y cálculos estadísticos |

---

## 📐 Diseño

El dashboard sigue principios de **consultoría estratégica**:
- Paleta de color corporativa por pivote
- Tipografía Inter (limpia, legible)
- Fondo neutro `#f7f9fc` con tarjetas blancas
- Semáforo de estado: 🟢 ≥80% · 🟡 50–79% · 🔴 <50%
- Hero banner con gradiente por pivote
- Completamente responsive (wide layout)

---

## 👥 Autores del Caso Original

Yıldırım, Tunçalp, İstanbullu, Konuşkan, İnan, Yasin, Apaçoğlu-Turan, Turan, Özer, Kerimoğlu — *Digitalization Cases Vol. 2*, Springer Nature, 2021.
