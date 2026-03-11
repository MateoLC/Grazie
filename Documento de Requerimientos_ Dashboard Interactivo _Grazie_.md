# **Documento de Requerimientos: Dashboard Interactivo "Grazie"**

## **1\. Objetivo del Proyecto**

Desarrollar una aplicación web interactiva (Dashboard) para la marca "Grazie" ([https://grazie.com.co/](https://grazie.com.co/)). La herramienta debe permitir el análisis ágil de los datos de ventas exportados desde Shopify, comparando el rendimiento histórico general con los resultados específicos del mes de abril, a través de una interfaz visualmente atractiva, premium y alineada con la identidad de la marca.

## **2\. Pila Tecnológica y "Skills" Requeridas**

El desarrollo se ejecutará utilizando el ecosistema de Python. El agente de IA (Antigravity) deberá inicializar obligatoriamente las siguientes *skills* del repositorio `sickn33/antigravity-awesome-skills/tree/main/skills`:

* **`data-scientist`**: Para la limpieza, agrupación y cálculo matemático de los CSV de Shopify utilizando `pandas`.  
* **`python-pro`**: Para asegurar un código modular, limpio y con buen manejo de excepciones en Python.  
* **`ui-ux-designer`**: Para estructurar el diseño visual, garantizar el uso correcto de espacios (padding/margin) y la aplicación de la paleta de colores.  
* **`context-fundamentals`**: Para que el agente mantenga el enfoque en la marca "Grazie" y no pierda de vista el objetivo corporativo a lo largo del código.

Librerías principales: `streamlit` (Framework web), `pandas` (Datos), `plotly` (Gráficos interactivos).

## **3\. Fuentes de Datos**

El sistema debe procesar los siguientes archivos CSV pre-cargados:

1. **Ventas Históricas:** `ventas Seria Shopify.xlsx - Hoja 1.csv`  
2. **Ventas de Abril:** `CG GENERAL Shopify Abril.xlsx - VENTAS ABRIL.csv` (y sus documentos consolidados asociados). *Nota técnica: El script debe incluir una función de limpieza para eliminar filas de subtotales o resúmenes al final de los archivos, además de gestionar celdas vacías (NaN).*

## **4\. Requerimientos de Diseño UI/UX (Identidad de Marca)**

El dashboard no debe parecer una plantilla genérica. Debe respirar la estética de **Grazie**:

* **Modo Visual:** Tema claro o un "Dark Mode" elegante (dependiendo de la legibilidad de los gráficos).  
* **Paleta de Colores Corporativa:**  
  * Color principal: Tonos terracota / ladrillo suave.  
  * Colores secundarios: Beige, crema, y neutros cálidos.  
  * Acentos para gráficos: Variaciones armónicas del terracota, dorados sutiles y grises oscuros para texto.  
* **Tipografía:** Fuentes Serif elegantes para encabezados (Títulos y KPIs) y Sans-Serif limpias para los ejes de los gráficos y tablas de datos.  
* **Interactividad:** Todos los gráficos deben tener *tooltips* al pasar el mouse (hover), opciones de zoom y descarga.

## **5\. Estructura y Gráficos del Dashboard**

La pantalla principal debe dividirse en dos pestañas o secciones principales navegables:

**Sección A: Visión Histórica (Global)**

* **Tarjetas KPI Superiores:** Ingresos Totales, Número de Pedidos, Ticket Promedio de todo el periodo.  
* **Gráfico 1 (Plotly Line Chart con Área):** Tendencia de ingresos mensuales a lo largo del tiempo. Color terracota con relleno semi-transparente.  
* **Gráfico 2 (Plotly Sunburst o Treemap):** Distribución de ventas por Estado de Pedido (Pagado, Pendiente, Reembolsado) o por Ciudad/Departamento.

**Sección B: Análisis Mes Actual (Abril)**

* **Tarjetas KPI Superiores:** Ingresos de Abril, Total de Unidades Vendidas (Ej: Gafas, Aretes, Pulseras).  
* **Gráfico 3 (Plotly Gauge Chart):** Medidor tipo velocímetro mostrando el cumplimiento de la meta de ventas de Abril.  
* **Gráfico 4 (Plotly Bar Chart Horizontal):** Top 10 de los productos/SKUs más vendidos en Abril, ordenados de mayor a menor.

