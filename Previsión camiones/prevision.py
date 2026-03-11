import random
import csv
import sqlite3
from datetime import date, timedelta
import os
import pandas as pd
from scipy.stats import binom
nombre=input("Escribe tu nombre de operador: ")
nombre=nombre[0:1].upper() + nombre[1:] #probando mayusculas
with sqlite3.connect("almacen.db") as conn: #se escribe asi porq esto no es python, es sql aunq lo escribamos aqui
    conn.execute(""" CREATE TABLE IF NOT EXISTS entregas ( 
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fecha DATE NOT NULL,
                 camiones INTEGER NOT NULL)""")
with sqlite3.connect("almacen.db") as conn:
    ultima_fecha=conn.execute("SELECT MAX(fecha) FROM entregas").fetchone()
    if ultima_fecha[0] is None:
        nueva_fecha=date.today()
    else:
        nueva_fecha=date.fromisoformat(ultima_fecha[0])+ timedelta(days=1) #sql tiene los datos en formato texto, por eso le decimos que lo traiga de ese formato al e pyhton
    camiones_simulados= random.randint(0,30)
    conn.execute(
        "INSERT INTO entregas (fecha, camiones) VALUES (?, ?)",
        (nueva_fecha.isoformat(), camiones_simulados) #pasamos a formato de sql, ya que lo teniamos de pyhton y lo vamos a meter en la data base
    )
    conn.commit() #para guardar las modificaciones que ha hecho esta conexion, la de arriba no hace falta porque no modifica, solo crea la tabla
#print(f"Fecha de simulación: {nueva_fecha}")
print(f"Camiones previstos: {camiones_simulados}")
camiones_reales=int(input(f"Hola {nombre}, escribe aqui las llegadas reales: "))
diferencia=camiones_reales-camiones_simulados
print(f"El {nueva_fecha}, los camiones previstos eran {camiones_simulados} y realmente llegaron {camiones_reales}")
print(f"La diferencia es de {diferencia} camiones")
if camiones_reales>=camiones_simulados:
    cumplimiento=1
else:
    cumplimiento=0
archivo="historico_entregas.csv"
existe=os.path.isfile(archivo) #comprueba si existe el archivo, si es asi devuelve true, sino false
with open(archivo,"a",newline="") as f:
    writer=csv.writer(f)
    if not existe: #es lo mismo que decir if not true (eso significa que es false, es decir no existe)
        writer.writerow(["Fecha","Previstos","Reales","Diferencia","Cumplimiento"])
    writer.writerow([nueva_fecha,camiones_simulados,camiones_reales, diferencia, cumplimiento])
print(f"Datos guardados en {archivo}")
print("\---INICIANDO ANALISIS DE DATOS---")
df=pd.read_csv(archivo)
print(df)
                      ### AHORA EMPEZAMOS A CALCULAR LOS KPIS ###
#Medias de los camiones
media_previstos=df["Previstos"].mean()
media_reales=df["Reales"].mean()
# Tasa de exito (es decir que llegen al menos los previstos). Como es bernouilli, es la media de Cumplimiento
probabilidad_exito=df["Cumplimiento"].mean()
print(f"La media de camiones previstos es de {media_previstos:.2f}") #son iguales pero esta mejor para imprimir
print(f"La media de camiones reales es de {round(media_reales,2)}") #y esta mejor para guardar datos
print(f"La probabilidad de exito es del {probabilidad_exito*100:.2f}%")

#PROBABILIDAD BINOMIAL (k,n,p) EJEMPLO DE: probabilidad de que de 5 dias, 4 coincida la prevision real y prevista
dias_futuros_n=5 #numero de ensayos
dias_objetivo_k=4 #numero de exitos que queremos lograr en los 5 días(ensayos)
prob_binomial=binom.pmf(dias_objetivo_k,dias_futuros_n,probabilidad_exito)
print(f"La probabilidad de cumplor la previsión excatamente {dias_objetivo_k} de los proximos {dias_futuros_n} futuros es del {prob_binomial*100:.2f}%")

#VARIANZAS Y DESVIACIONES
varianzas_reales=df["Reales"].var() #lo que se alejan los datos de la media al cuadrado
desviacion_reales=df["Reales"].std() 
print(f"La varianza de llegadas es de {varianzas_reales:.2f}")
print(f"Desviación estandar de {desviacion_reales:.2f} camiones") #cuanto mas alto más inestable
#RANGOS (MEDIA+-DESVIACIÓN TÍPICA)
rango_inferior=media_reales-desviacion_reales
rango_superior=media_reales+desviacion_reales
print(f"Una operativa estable se situa entre {rango_inferior:.2f} y {rango_superior:.2f} camiones")
if desviacion_reales>10:
    print("Estado caótico con mucha variación de datos y muy dificil de predecir")
elif desviacion_reales>5:
    print("Hay cierta inestabilidad con variaciones moderadas")
else:
    print("El flujo de camiones es muy estable")

        ### AHORA EXPORTAREMOS KPI PARA PODER MOSTRARLOS EN POWER BI ###
datos_kpi={              #aqui estamos creando el diccionario 
    "Media_Previstos":[round(media_previstos,2)],
    "Media_Reales":[round(media_reales,2)],
    "Probabilidad_Exito_Pct":[round(probabilidad_exito*100,2)],
    "Desviación_Estandar":[round(desviacion_reales,2)],
    "Rango_Inferior":[round(rango_inferior,2)],
    "Rango_Superior":[round(rango_superior,2)]
    }
df_kpis=pd.DataFrame(datos_kpi) #TENEMOS QUE CONVERTIR EL DICCIONARIO EN UN DATAFRAME  PARA  ASI CONVERTIR LOS DATOS SUELTOS DEL DICCIONARIO EN UNA TABLA
archivo_kpis="resumen_kpis.csv"
df_kpis.to_csv(archivo_kpis,index=False, sep=",",decimal=",dd") #pasamos el dataframe a csv, guardandola como archivo_kpis que es resumen_kpis.csv, y el index fasle es para que no tenga indice la tabla
print(f"Archivo KPIS exportado correctamente a {archivo_kpis}")