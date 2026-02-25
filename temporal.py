import pandas as pd
import numpy as np
df = pd.read_csv("incidentes_crue_diarios.txt", sep="\s+")

print(df.columns)

df["fecha"]=pd.to_datetime(df["fecha"])

df["año"] = df["fecha"].dt.year

promedio_anual = df.groupby("año")["incidentes"].mean()

prom_2022 = promedio_anual[2022]
prom_2023 = promedio_anual[2023]
diferencia = prom_2023 - prom_2022

print("Promedio 2022:", prom_2022)
print("Promedio 2023:", prom_2023)
print("Diferencia (2023-2022):", diferencia)

dias = {0:"Lunes", 1:"Martes", 2:"Miércoles", 3:"Jueves", 4:"Viernes", 5:"Sábado", 6:"Domingo"}
df["dia_semana"] = df["fecha"].dt.dayofweek.map(dias)
promedio_dia = df.groupby("dia_semana")["incidentes"].mean()

print("Lunes:", promedio_dia["Lunes"])
print("Martes:", promedio_dia["Martes"])
print("Miércoles:", promedio_dia["Miércoles"])
print("Jueves:", promedio_dia["Jueves"])
print("Viernes:", promedio_dia["Viernes"])
print("Sábado:", promedio_dia["Sábado"])
print("Domingo:", promedio_dia["Domingo"])
print("Día con MÁS incidentes:", promedio_dia.idxmax())

meses = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio",
         7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
df["mes"] = df["fecha"].dt.month.map(meses)

promedio_mes = df.groupby("mes")["incidentes"].mean().sort_values(ascending=False)

print("Mes #1 (más alto):", promedio_mes.index[0], "-", promedio_mes.iloc[0])
print("Mes #2:", promedio_mes.index[1], "-", promedio_mes.iloc[1])
print("Mes #3:", promedio_mes.index[2], "-", promedio_mes.iloc[2])
print("Mes más BAJO:", promedio_mes.index[-1], "-", promedio_mes.iloc[-1])
