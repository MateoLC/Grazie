"Actúa como un Desarrollador Full-Stack y Científico de Datos Senior. Antes de escribir cualquier código, asegúrate de aplicar las siguientes skills de tu directorio: `data-scientist`, `python-pro`, `ui-ux-designer` y `context-fundamentals`.

**Tu objetivo:** Desarrollar el código completo de un dashboard web interactivo en Python utilizando Streamlit y Plotly para mi cliente, la marca de moda y accesorios 'Grazie' (inspirado en grazie.com.co).

**Datos disponibles (ya en tu contexto):**

1. 'ventas Seria Shopify.xlsx \- Hoja 1.csv' (Histórico)  
2. 'CG GENERAL Shopify Abril.xlsx \- VENTAS ABRIL.csv' (Mes específico). *Importante para data-scientist:* Limpia los DataFrames eliminando filas de totales al final del CSV de abril y maneja correctamente los formatos de fecha y moneda.

**Reglas de UI/UX y Diseño (ui-ux-designer):** La interfaz debe ser premium. Configura Streamlit y Plotly para usar una paleta de colores corporativa: tonos terracota, beige y neutros cálidos. Usa una tipografía Serif para títulos/KPIs y Sans-Serif para datos. Modifica el layout de Streamlit a 'wide'.

**Estructura requerida:**

1. Un Sidebar para filtros globales (Rango de fechas y Ciudad).  
2. Dos pestañas (Tabs): 'Histórico General' y 'Análisis Abril'.  
3. En 'Histórico': Genera KPIs (Métricas con deltas), un gráfico de líneas con área rellenada para tendencias de ventas a lo largo del tiempo, y un gráfico de dona para el estado financiero de los pedidos.  
4. En 'Análisis Abril': Genera un Gauge Chart (medidor) para la meta de ventas mensual, y un gráfico de barras horizontales mostrando el Top 10 de productos más vendidos.

Todos los gráficos deben ser generados con `plotly.express` o `plotly.graph_objects` para asegurar máxima interactividad (tooltips, hover). Por favor, genera el script completo `app.py` listo para ejecutarse."

