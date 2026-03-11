import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts

# ==========================================
# 1. UI/UX CONFIGURATION & CSS INJECTION
# ==========================================
st.set_page_config(
    page_title="Dashboard de Ventas Grazie",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Color Palette Grazie
COLOR_BG = "#FDFBF7"        # Wamer Cream
COLOR_CARD = "#FFFFFF"      # Pure White for cards
COLOR_TEXT = "#2C2C2C"      # Dark Gray
COLOR_TERRACOTTA = "#C85A44"# Main brand color
COLOR_GOLD = "#D4AF37"      # Accent Gold
COLOR_GRAY = "#888888"      # Secondary Text

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

    /* CSS Reset & Background */
    .stApp {{
        background-color: {COLOR_BG};
    }}
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_TEXT};
    }}
    
    /* Hide Streamlit Top Menu & Footer */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* Typography Hierarchy */
    h1, h2, h3, h4 {{
        font-family: 'Playfair Display', serif !important;
        color: {COLOR_TERRACOTTA} !important;
        margin-bottom: 0.5rem;
    }}
    
    h1 {{ font-size: 2.8rem; font-weight: 600; border-bottom: 2px solid {COLOR_GOLD}; padding-bottom: 10px; margin-bottom: 2rem; }}
    h2 {{ font-size: 2.2rem; margin-top: 3rem; margin-bottom: 1rem; color: {COLOR_TEXT} !important; }}
    
    /* Custom KPI Cards & Fade-In Animation */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    div[data-testid="metric-container"] {{
        background-color: {COLOR_CARD};
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(200, 90, 68, 0.08); /* Subtle Terracotta Shadow */
        border: 1px solid rgba(212, 175, 55, 0.2); /* Subtle Gold border */
        animation: fadeIn 0.8s ease-out forwards;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(200, 90, 68, 0.15);
    }}
    
    div[data-testid="metric-value"] {{
        color: {COLOR_TEXT};
        font-weight: 600;
        font-family: 'Inter', sans-serif !important;
        font-size: 2.2rem !important;
    }}
    
    .block-container {{
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}
    
    /* Custom Button Styling */
    div.stButton > button:first-child {{
        background-color: {COLOR_TERRACOTTA};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(200, 90, 68, 0.2);
    }}
    
    div.stButton > button:first-child:hover {{
        background-color: {COLOR_GOLD};
        color: {COLOR_TEXT};
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(212, 175, 55, 0.3);
    }}
    
    /* Section Dividers */
    hr {{
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(200, 90, 68, 0), rgba(200, 90, 68, 0.75), rgba(200, 90, 68, 0));
        margin: 3rem 0;
    }}
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA PROCESSING (Google Drive API)
# ==========================================

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json.json'
ID_HISTORICAL = '1qTZpOe6-hLSGpJ1KPdt9rdufrG455xVxj3dHAnxJhlg'
ID_APRIL = '1ucDXMHOmn3GMcQCcFnmjRNjPyZIuYTehC-ImxCCCTqI'

@st.cache_resource
def get_drive_service():
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"Error authenticating with Google Drive: {e}")
        return None

@st.cache_data(ttl=3600) # Cache for 1 hour
def download_excel_from_drive(_service, file_id):
    try:
        # Try to export native Google Sheets as Excel
        request = _service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return pd.read_excel(fh)
    except Exception as e:
        # Fallback for standard binary Excel uploads
        try:
            request = _service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return pd.read_excel(fh)
        except Exception as e2:
            st.error(f"Error downloading file {file_id}: {e2}")
            return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_historical_data():
    service = get_drive_service()
    if service is None: return pd.DataFrame()
    
    df = download_excel_from_drive(service, ID_HISTORICAL)
    if df.empty: return df
    
    df = df.dropna(how='all')
    if 'precio' in df.columns:
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df = df.dropna(subset=['created_at', 'precio'])
    return df

@st.cache_data(ttl=3600)
def load_april_data():
    service = get_drive_service()
    if service is None: return pd.DataFrame()
        
    df = download_excel_from_drive(service, ID_APRIL)
    if df.empty: return df
    
    df = df.dropna(how='all')
    cols = ['Lineitem price', 'Suma de Lineitem quantity', 'Total']
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    
    if 'Lineitem sku' in df.columns and 'Total' in df.columns:
        df = df.dropna(subset=['Lineitem sku', 'Total'])
        df = df[~df['Lineitem sku'].astype(str).str.contains('total general', case=False, na=False)]
    return df

df_hist = load_historical_data()
df_april = load_april_data()

# Header con botón alineado a la derecha
col_title, col_btn = st.columns([5, 1])
with col_title:
    st.markdown("<h1>Dashboard Ejecutivo Grazie</h1>", unsafe_allow_html=True)
with col_btn:
    st.markdown("<div style='margin-top: 2rem; display: flex; justify-content: flex-end;'>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Helper function to check data
if df_hist.empty or df_april.empty:
    st.error("Error conectando con Google Drive o procesando los datos. Verifique los permisos del archivo `credentials.json.json`.")
    st.stop()


# ==========================================
# SECCIÓN 1: EL PANORAMA HISTÓRICO
# ==========================================
st.markdown("<h2>1. El Panorama Histórico (Acumulado)</h2>", unsafe_allow_html=True)

# KPI HISTÓRICOS
total_revenue_hist = df_hist['precio'].sum()
total_orders_hist = df_hist['order_number'].nunique() if 'order_number' in df_hist.columns else len(df_hist)
avg_ticket_hist = total_revenue_hist / total_orders_hist if total_orders_hist > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Históricos Totales", f"${total_revenue_hist:,.0f}")
col2.metric("Total de Pedidos", f"{total_orders_hist:,}")
col3.metric("Ticket Promedio Global", f"${avg_ticket_hist:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# Gráfico Principal Animado (Spline Area Chart)
# Agrupar ventas totales Día a Día para suavizar la curva
# Agrupar ventas totales Día a Día para suavizar la curva
df_hist['Fecha'] = df_hist['created_at'].dt.strftime('%Y-%m-%d')
hist_daily = df_hist.groupby('Fecha')['precio'].sum().reset_index()
hist_daily = hist_daily.sort_values('Fecha')
time_data_list = hist_daily.values.tolist()

option_spline = {
    "backgroundColor": "transparent",
    "title": {
        "text": "Histórico de Ventas (Transacciones Individuales)",
        "left": "center",
        "textStyle": {"color": COLOR_TERRACOTTA, "fontFamily": "Playfair Display", "fontSize": 18, "fontWeight": "normal"}
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": { "type": "line" }
    },
    "xAxis": {
        "type": "time",
        "axisLine": {"lineStyle": {"color": COLOR_TEXT}},
        "axisTick": {"show": False},
        "splitLine": {"show": False}
    },
    "yAxis": {
        "type": "value",
        "axisLine": {"show": False},
        "axisTick": {"show": False},
        "splitLine": {"lineStyle": {"color": "rgba(212, 175, 55, 0.15)", "type": "dashed"}},
        "axisLabel": {"formatter": "${value}"}
    },
    "series": [
        {
            "data": time_data_list,
            "type": "line",
            "smooth": True, # Spline curve
            "symbol": "circle",
            "symbolSize": 8,
            "itemStyle": {"color": COLOR_TERRACOTTA},
            "lineStyle": {"width": 4, "color": COLOR_TERRACOTTA},
            "areaStyle": {
                "color": {
                    "type": 'linear',
                    "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "rgba(200, 90, 68, 0.7)"}, # Terracotta Top
                        {"offset": 1, "color": "rgba(200, 90, 68, 0.0)"}  # Transparent Bottom
                    ]
                }
            },
            "animationDuration": 2500, # Beautiful fade-draw in
            "animationEasing": "cubicInOut"
        }
    ]
}

st_echarts(options=option_spline, height="450px")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================
# SECCIÓN 2: LUPA EN ABRIL
# ==========================================
st.markdown("<h2>2. Lupa en Mes Actual</h2>", unsafe_allow_html=True)

april_revenue = df_april['Total'].sum()
april_units = df_april['Suma de Lineitem quantity'].sum()

colA, colB = st.columns(2)
colA.metric("Ingresos Mes Actual", f"${april_revenue:,.0f}")
colB.metric("Unidades Vendidas", f"{april_units:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# Gráficos Abril: Top 10 y Dona
c2_left, c2_right = st.columns([1.5, 1])

with c2_left:
    # Aggregating Top 10 Products
    top_products = df_april.groupby('Lineitem name').agg({'Total': 'sum'}).reset_index()
    top10 = top_products.sort_values(by='Total', ascending=True).tail(10) # Ascending for Echarts horizontal bar
    
    option_bar = {
        "backgroundColor": "transparent",
        "title": {
            "text": "Top 10 Productos Más Vendidos",
            "textStyle": {"color": COLOR_TEXT, "fontFamily": "Inter", "fontSize": 16, "fontWeight": "normal"}
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {"type": 'shadow'}
        },
        "grid": {"left": '3%', "right": '4%', "bottom": '3%', "containLabel": True},
        "xAxis": {
            "type": 'value',
            "splitLine": {"lineStyle": {"color": "rgba(212, 175, 55, 0.1)", "type": "dashed"}},
        },
        "yAxis": {
            "type": 'category',
            "data": top10['Lineitem name'].tolist(),
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {
                "fontSize": 10
            }
        },
        "series": [
            {
                "name": 'Ingresos ($)',
                "type": 'bar',
                "data": top10['Total'].tolist(),
                "itemStyle": {"color": COLOR_GOLD, "borderRadius": [0, 5, 5, 0]},
                "emphasis": {
                    "itemStyle": {"color": COLOR_TERRACOTTA} # Changes to Terracotta on hover
                },
                "animationDuration": 1500,
                "animationDelay": 'lambda idx: idx * 100' # Sequential loading
            }
        ]
    }
    st_echarts(options=option_bar, height="400px")

with c2_right:
    # Donut Chart for Top 5 Products by Units Sold
    if not df_april.empty and 'Suma de Lineitem quantity' in df_april.columns:
        top_units = df_april.groupby('Lineitem name').agg({'Suma de Lineitem quantity': 'sum'}).reset_index()
        top5_units = top_units.sort_values(by='Suma de Lineitem quantity', ascending=False).head(5)
        
        data_donut = [{"value": int(row['Suma de Lineitem quantity']), "name": row['Lineitem name'][:15] + '...'} for index, row in top5_units.iterrows()]
    else:
        data_donut = []
    
    option_donut = {
        "backgroundColor": "transparent",
        "title": {
            "text": "Top 5 Productos (Unidades)",
            "left": "center",
            "textStyle": {"color": COLOR_TEXT, "fontFamily": "Inter", "fontSize": 16, "fontWeight": "normal"}
        },
        "tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b}: {c} unidades ({d}%)', "confine": True},
        "legend": {
            "orient": 'horizontal',
            "bottom": '0',
            "itemWidth": 12,
            "textStyle": {"color": COLOR_TEXT}
        },
        "series": [
            {
                "name": 'Unidades Vendidas',
                "type": 'pie',
                "radius": ['45%', '70%'],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 5,
                    "borderColor": COLOR_BG,
                    "borderWidth": 2
                },
                "label": {"show": False, "position": 'center'},
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": '13',
                        "fontWeight": 'normal',
                        "color": '#000000',
                        "fontFamily": "Inter",
                        "formatter": '{b}\n{c} unids.'
                    }
                },
                "labelLine": {"show": False},
                "data": data_donut,
                "color": [COLOR_TERRACOTTA, COLOR_GOLD, COLOR_GRAY, '#E4C7B7', '#D2B48C'],
                "animationDuration": 2000,
                "animationEasing": "cubicOut"
            }
        ]
    }
    st_echarts(options=option_donut, height="400px")

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# SECCIÓN 3: LA COMPARACIÓN (El Cara a Cara)
# ==========================================
st.markdown("<h2>3. El Cara a Cara: Histórico vs Mes Actual</h2>", unsafe_allow_html=True)

st.markdown("<p style='font-size: 1.1rem; color: #666;'>Comparación de ingresos netos del Mes Actual versus el mes más exitoso registrado en el histórico de la marca.</p>", unsafe_allow_html=True)

# Data prep for comparison (Best Historical Month vs April)
df_hist['Month_str'] = df_hist['created_at'].dt.strftime('%B %Y')
monthly_hist = df_hist.groupby('Month_str')['precio'].sum().reset_index()
best_hist_month = monthly_hist.loc[monthly_hist['precio'].idxmax()]
best_month_name = best_hist_month['Month_str']
best_month_revenue = best_hist_month['precio']

# Calculate difference
diff_pct = ((april_revenue / best_month_revenue) - 1) * 100 if best_month_revenue > 0 else 0
diff_color = COLOR_TERRACOTTA if diff_pct > 0 else COLOR_GRAY
diff_sign = "+" if diff_pct > 0 else ""

option_comparison = {
    "backgroundColor": "transparent",
    "title": {
        "text": f"Diferencia: {diff_sign}{diff_pct:,.1f}% vs Mejor Mes",
        "left": "center",
        "top": 0,
        "textStyle": {"color": diff_color, "fontFamily": "Inter", "fontSize": 16, "fontWeight": "bold"}
    },
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": {
            "type": 'shadow'
        },
        "formatter": '{b}: ${c}'
    },
    "grid": {
        "left": '10%',
        "right": '10%',
        "bottom": '15%',
        "top": '15%',
        "containLabel": True
    },
    "xAxis": {
        "type": 'category',
        "data": [f'Récord Histórico\n({best_month_name})', 'Rendimiento\nMes Actual'],
        "axisTick": {"alignWithLabel": True, "show": False},
        "axisLine": {"lineStyle": {"color": "rgba(212, 175, 55, 0.4)"}},
        "axisLabel": {
            "color": COLOR_TEXT,
            "fontFamily": "Inter",
            "fontSize": 14,
            "fontWeight": "bold"
        }
    },
    "yAxis": {
        "type": 'value',
        "splitLine": {"lineStyle": {"color": "rgba(212, 175, 55, 0.15)", "type": "dashed"}},
        "axisLabel": {"formatter": "${value}"}
    },
    "series": [
        {
            "name": 'Ingresos',
            "type": 'bar',
            "barWidth": '40%',
            "data": [
                {
                    "value": int(best_month_revenue),
                    "label": {"show": True, "formatter": f"${int(best_month_revenue):,}"},
                    "itemStyle": {"color": COLOR_GOLD, "borderRadius": [8, 8, 0, 0]}
                },
                {
                    "value": int(april_revenue),
                    "label": {"show": True, "formatter": f"${int(april_revenue):,}"},
                    "itemStyle": {"color": COLOR_TERRACOTTA, "borderRadius": [8, 8, 0, 0]}
                }
            ],
            "label": {
                "show": True,
                "position": 'top',
                "color": COLOR_TEXT,
                "fontFamily": "Inter",
                "fontWeight": "bold",
                "fontSize": 14
            },
            "animationDuration": 2500,
            "animationEasing": "cubicOut"
        }
    ]
}

# Render the bar chart wide and prominent
c3_1, c3_2, c3_3 = st.columns([1, 4, 1])
with c3_2:
    st_echarts(options=option_comparison, height="500px")
