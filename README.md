# Gestión de Flujos Logísticos: Análisis de Desviaciones y Estabilidad Operativa (LLegadas Reales Vs Previstas)

Este proyecto es una herramienta de **Business Intelligence** desarrollada en Python. Su objetivo es monitorizar la eficiencia de un centro logístico comparando la planificación (camiones previstos) con la operativa real (camiones que han llegado), detectando así niveles de inestabilidad mediante análisis estadístico.

## Propósito del Proyecto y lógica de negocio
En el sector de la **Logística y Supply Chain**, la variabilidad es el factor que más encarece la operativa, ya que un flujo inestable puede provocar sobrecoste por horas extra o tiempos muertos, cuellos de botella por saturación de muelles o falta de fiabilidad en la previsión que genera incapacidad para comprometrse con plazos de entrega.
Este programa no solo registra datos, sino que evalúa la **estabilidad del almacén**. Un flujo con alta desviación estándar indica una operativa caótica, dificultando la planificación de recursos humanos y maquinaria. Algunos días llegan ***muchos*** camiones, saturando muelles y generando horas extra; otros días llegan ***pocos***, dejando personal y recursos infrautilizados.
En ***ambos casos se producen sobrecostes*** operativos.
## Estructura de Archivos y Flujo de Datos

Para el correcto funcionamiento del sistema, el proyecto se organiza en los siguientes archivos:

* **`prevision.py`**: Es el motor principal del proyecto. Contiene la lógica de conexión a la base de datos, el simulador de llegadas, el procesamiento estadístico con Pandas y la generación de diagnósticos.
* **`almacen.db`**: Base de datos relacional (SQLite). Almacena de forma persistente la fecha de cada operativa y el número de camiones simulados, garantizando la integridad de la línea temporal.
* **`historico_entregas.csv`**: Registro histórico detallado. Almacena cada jornada con sus datos de previsión, realidad, diferencia y cumplimiento. Es la fuente de datos principal para el análisis de Pandas.
* **`resumen_kpis.csv`**: Archivo de salida optimizado. Contiene los resultados del análisis (medias, desviaciones y probabilidades) listo para ser importado en herramientas de visualización como Power BI o Excel.

## Funcionalidades Clave

### 1. Gestión Inteligente de Datos (SQL + CSV)
El sistema utiliza **SQLite** para asegurar la integridad de la línea temporal, calculando automáticamente la fecha siguiente a la última registrada. Los datos se exportan a un histórico CSV para mantener un registro auditable de cada jornada.

### 2. Análisis Estadístico y KPIs
El motor de análisis calcula automáticamente:
* **Tasa de Cumplimiento (Bernoulli):** Porcentaje de días en los que se alcanzó el objetivo previsto.
* **Probabilidad Binomial:** Calcula la probabilidad exacta de éxito en escenarios futuros (ej: *"¿Qué probabilidad hay de cumplir el objetivo 4 de los próximos 5 días?"*).
* **Análisis de Variabilidad:** Uso de **Varianza** y **Desviación Estándar** para diagnosticar la salud del flujo logístico.

### 3. Diagnóstico de Operativa
El programa categoriza el estado del almacén en tiempo real:
* **Estable:** Flujo constante y predecible.
* **Inestable:** Variaciones moderadas que requieren atención.
* **Estado Caótico:** Alta variabilidad que impide una planificación eficiente.

El cálculo del estado se realiza mediante el Coeficiente de Variación (CV), que se define como el cociente entre la desviación estándar sigma y la media mu, siguiendo la fórmula CV =sigma\mu; se considera que los datos son homogéneos si el resultado es menor o igual al 30%, mientras que un valor superior indica que los datos son heterogéneos y presentan una alta dispersión. En nuestro caso como **tenemos 3 estados**, hemos ajustado los porcentajes y hemos considerado entre **0%-25%, entre 25%-50% y más del 50%**. En cualquier caso ***se podrian modificar*** según las necesidades

El rango de operativa estable se define estadísticamente como el intervalo donde se concentra el 68% de la actividad habitual (Media ± 1 Desviación Estándar), permitiendo identificar cualquier desviación fuera de estos límites como una anomalía operativa.


### 4. Preparado para Power Bi
El script genera un archivo `resumen_kpis.csv` optimizado. Este archivo está diseñado para ser importado directamente en herramientas de visualización de datos, permitiendo la creación de dashboards corporativos.

## 5.Ejemplo de Salida (datos inventados)
```text
--- INICIANDO ANÁLISIS DE DATOS ---
El 2026-04-20, los camiones previstos eran 13 y realmente llegaron 15
La diferencia es de 2 camiones
La media de camiones previstos es de 14.50
La media de camiones reales es de 16,2
La probabilidad de éxito es del 60.00%
La probabilidad de cumplir la previsión exactamente 4 de los próximos 5 días es del 25.92%
Desviación estándar de 8.45 camiones
Una operativa estable si situa entre 7.06 y 10,08 camiones (Intervalo de Confianza)
> "Hay cierta inestabilidad con variaciones moderadas"
Archivo KPIS exportado correctamente a resumen_kpis.csv
```
### **Desarrollado por Sergio Ruiz Gutiérrez**
*Optimización de Procesos y Análisis de Datos aplicados a la Supply Chain*
