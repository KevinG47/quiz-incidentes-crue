# Análisis Descriptivo de Incidentes CRUE

## Descripción de los datos
Este proyecto analiza los incidentes diarios reportados al CRUE (Centro Regulador de Urgencias y Emergencias).
El dataset contiene 730 registros diarios correspondientes al período del 1 de enero de 2022 al 31 de diciembre de 2023,
con dos variables: fecha e incidentes.

## Colaboradores

| Nombre | GitHub |
|--------|--------|
| Kevin Leonardo Chaparro Reyes | [@KevinG47](https://github.com/KevinG47) |
| Valentina Palma | [@pinkandredval](https://github.com/pinkandredval) |

## Hallazgos principales

| Estadística | Valor |
|-------------|-------|
| Media diaria | 1717.47 incidentes |
| Mediana | 1711.0 incidentes |
| Desviación estándar | 256.31 |
| Valor máximo | 3275 incidentes (2022-12-25) |
| Valor mínimo | 935 incidentes (2022-04-15) |
| Rango intercuartílico (IQR) | 299.5 |
| Promedio 2022 | 1667.10 incidentes/día |
| Promedio 2023 | 1767.85 incidentes/día |
| Día con más incidentes | Domingo (promedio 1880.04) |
| Mes con más incidentes | Diciembre (promedio 1881.02) |

## ¿Se puede predecir?
Aunque se identifican patrones como el aumento de incidentes los fines de semana y en diciembre, consideramos que una predicción precisa es difícil debido a variables externas como días sin carro, eventos masivos o partidos de fútbol, que generan picos atípicos que un modelo basado solo en fechas no podría anticipar.
