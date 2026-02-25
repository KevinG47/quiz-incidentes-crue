import pandas as pd
import numpy as np
df = pd.read_csv("incidentes_crue_diarios.txt", sep="\s+")

print(df.columns)

serie = df["incidentes"]

media = serie.mean()
mediana = serie.median()
moda = serie.mode()[0]

print("Media:", media)
print("Mediana:", mediana)
print("Moda:", moda)


desviacion = serie.std()
varianza = serie.var()
cv = (desviacion / media) * 100
rango = serie.max() - serie.min()

print("Desviación estándar:", desviacion)
print("Varianza:", varianza)
print("Coeficiente de variación:", cv, "%")
print("Rango:", rango)

Q1 = serie.quantile(0.25)
Q2 = serie.quantile(0.50)
Q3 = serie.quantile(0.75)
IQR = Q3 - Q1
P95 = serie.quantile(0.95)

print("Q1 (percentil 25):", Q1)
print("Q2 (mediana):", Q2)
print("Q3 (percentil 75):", Q3)
print("Rango intercuartílico (IQR):", IQR)
print("Percentil 95:", P95)

dia_max = df.loc[serie.idxmax(), "fecha"]
valor_max = serie.max()
dia_min = df.loc[serie.idxmin(), "fecha"]
valor_min = serie.min()

print("Día con MÁS incidentes:", dia_max)
print("Valor máximo:", valor_max)
print("Día con MENOS incidentes:", dia_min)
print("Valor mínimo:", valor_min)