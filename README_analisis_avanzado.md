# Análisis de Incidentes Diarios CRUE 2022-2023

## Descripción del proyecto
Este proyecto realiza un análisis estadístico completo de los incidentes diarios reportados al CRUE (Centro Regulador de Urgencias y Emergencias) durante el período del 1 de enero de 2022 al 31 de diciembre de 2023. El dataset contiene 730 registros diarios con dos variables: fecha e incidentes.

---

## Colaboradores

| Nombre | GitHub | Aporte |
|--------|--------|--------|
| Kevin Leonardo Chaparro Reyes | [@KevinG47](https://github.com/KevinG47) | Análisis descriptivo + Análisis avanzado |
| Valentina Palma | [@pinkandredval](https://github.com/pinkandredval) | Análisis temporal |

---

## Archivos del proyecto

| Archivo | Descripción |
|---------|-------------|
| `descriptivo.py` | Estadísticas descriptivas básicas |
| `agregados.py` | Análisis avanzado, gráficos y modelo SARIMA |
| `incidentes_crue_diarios.txt` | Base de datos original |

---

## 1. Estadísticas Descriptivas

### Medidas de tendencia central

| Estadística | Valor |
|-------------|-------|
| Media diaria | 1717.47 incidentes |
| Mediana | 1711.0 incidentes |
| Moda | 1812 incidentes |

### Medidas de dispersión

| Estadística | Valor | Interpretación |
|-------------|-------|----------------|
| Desviación estándar | 256.31 | Los datos se alejan en promedio 256 incidentes de la media |
| Varianza | 65694.62 | — |
| Coeficiente de variación | 14.92% | Dispersión baja-moderada, los datos son relativamente homogéneos |
| Rango | 2340 | Diferencia entre el día más alto y el más bajo |

### Cuartiles y Percentiles

| Medida | Valor | Interpretación |
|--------|-------|----------------|
| Q1 (percentil 25) | 1559.5 | El 25% de los días tuvo menos de 1559 incidentes |
| Q2 (mediana) | 1711.0 | El 50% de los días tuvo menos de 1711 incidentes |
| Q3 (percentil 75) | 1859.0 | El 75% de los días tuvo menos de 1859 incidentes |
| IQR | 299.5 | Rango del 50% central de los datos |
| Percentil 95 | 2081.75 | Solo el 5% de los días superó 2081 incidentes |

### Valores Extremos

| | Fecha | Valor |
|-|-------|-------|
| Día con MÁS incidentes | 2022-12-25 (Navidad) | 3275 |
| Día con MENOS incidentes | 2022-04-15 (Viernes Santo) | 935 |

---

## 2. Análisis Temporal

### Promedio por año

| Año | Promedio diario | Diferencia |
|-----|----------------|------------|
| 2022 | 1667.10 | — |
| 2023 | 1767.85 | +100.75 (+6%) |

### Promedio por día de la semana

| Día | Promedio |
|-----|----------|
| Lunes | 1632.06 |
| Martes | 1624.73 |
| Miércoles | 1621.72 |
| Jueves | 1665.93 |
| Viernes | 1762.36 |
| Sábado | 1832.81 |
| **Domingo** | **1880.04** |

### Top meses por promedio de incidentes

| Posición | Mes | Promedio |
|----------|-----|----------|
| 🥇 Más alto | Diciembre | 1881.02 |
| 🥈 | Septiembre | 1844.60 |
| 🥉 | Noviembre | 1794.78 |
| 🔻 Más bajo | Enero | 1460.61 |

---

## 3. Prueba de Hipótesis: ¿El domingo tiene significativamente más incidentes?

Para responder esta pregunta con respaldo estadístico, se siguió un protocolo de verificación de supuestos antes de elegir cada prueba.

### Paso 1 — Prueba de Normalidad: Shapiro-Wilk

**¿Por qué esta prueba?**
Antes de cualquier comparación estadística es necesario saber si los datos siguen una distribución normal, ya que esto determina si se pueden usar pruebas paramétricas (como ANOVA) o no paramétricas.

**Supuestos de Shapiro-Wilk:**
- Los datos deben ser continuos o al menos ordinales
- Se aplica por grupo de forma independiente
- H0: los datos siguen una distribución normal
- H1: los datos NO siguen una distribución normal

**Resultados:**

| Día | p-valor | Conclusión |
|-----|---------|------------|
| Lunes | 0.0000 | No normal |
| Martes | 0.6836 | Normal ✓ |
| Miércoles | 0.0024 | No normal |
| Jueves | 0.0000 | No normal |
| Viernes | 0.0000 | No normal |
| Sábado | 0.0061 | No normal |
| Domingo | 0.0000 | No normal |

**Decisión:** Como 6 de 7 días no cumplen normalidad, no se puede usar ANOVA paramétrico.

---

### Paso 2 — Prueba de Homocedasticidad: Levene

**¿Por qué esta prueba?**
La homocedasticidad (igualdad de varianzas entre grupos) es un supuesto adicional requerido por pruebas paramétricas como ANOVA. Se verificó para tener un diagnóstico completo.

**Supuestos de Levene:**
- Independencia entre grupos
- H0: las varianzas de todos los grupos son iguales
- H1: al menos un grupo tiene varianza diferente

**Resultado:**

| Prueba | p-valor | Conclusión |
|--------|---------|------------|
| Levene | 0.0457 | Varianzas diferentes |

**Decisión:** Las varianzas son significativamente diferentes, lo que confirma que no se puede usar ANOVA.

---

### Paso 3 — Prueba principal: Kruskal-Wallis

**¿Por qué esta prueba?**
Al no cumplirse normalidad ni homocedasticidad, se optó por la alternativa no paramétrica de ANOVA: Kruskal-Wallis, que compara medianas entre grupos sin asumir distribución normal ni igualdad de varianzas.

**Supuestos de Kruskal-Wallis:**
- Independencia de las observaciones entre grupos ✅
- Variable dependiente continua o al menos ordinal ✅ (incidentes es continua)
- Variable independiente con 3 o más grupos categóricos ✅ (7 días de la semana)
- Distribuciones de forma similar entre grupos ✅ (verificado con gráfico de densidad KDE: todas las curvas son unimodales y aproximadamente simétricas, solo desplazadas)

**Resultado:**

| Estadístico | p-valor | Conclusión |
|-------------|---------|------------|
| 147.6533 | 0.0000 | Sí hay diferencia significativa entre los días ✓ |

**Decisión:** Se rechaza H0. Hay al menos un día significativamente diferente. Se procede con prueba post-hoc.

---

### Paso 4 — Prueba Post-Hoc: Mann-Whitney con corrección de Bonferroni

**¿Por qué esta prueba?**
Kruskal-Wallis solo indica que *algún* grupo es diferente, pero no cuál. El post-hoc de Mann-Whitney compara todos los pares de días para identificar cuáles son significativamente distintos entre sí.

**Supuestos:**
- Independencia de las observaciones ✅
- Datos al menos ordinales ✅
- Se aplica tras un resultado significativo de Kruskal-Wallis ✅
- No requiere normalidad ni homocedasticidad ✅
- Corrección de Bonferroni para controlar el error tipo I en comparaciones múltiples ✅ (alpha corregido = 0.05 / 21 comparaciones = 0.0024)

**Resultados:**

| Comparación | p-valor | Resultado |
|-------------|---------|-----------|
| Lunes vs Martes | 0.8565 | Sin diferencia |
| Lunes vs Miércoles | 0.8294 | Sin diferencia |
| Lunes vs Jueves | 0.1922 | Sin diferencia |
| Lunes vs Viernes | 0.0000 | Diferencia significativa ✓ |
| Lunes vs Sábado | 0.0000 | Diferencia significativa ✓ |
| Lunes vs Domingo | 0.0000 | Diferencia significativa ✓ |
| Martes vs Miércoles | 0.6885 | Sin diferencia |
| Martes vs Jueves | 0.2030 | Sin diferencia |
| Martes vs Viernes | 0.0000 | Diferencia significativa ✓ |
| Martes vs Sábado | 0.0000 | Diferencia significativa ✓ |
| Martes vs Domingo | 0.0000 | Diferencia significativa ✓ |
| Miércoles vs Jueves | 0.1116 | Sin diferencia |
| Miércoles vs Viernes | 0.0000 | Diferencia significativa ✓ |
| Miércoles vs Sábado | 0.0000 | Diferencia significativa ✓ |
| Miércoles vs Domingo | 0.0000 | Diferencia significativa ✓ |
| Jueves vs Viernes | 0.0001 | Diferencia significativa ✓ |
| Jueves vs Sábado | 0.0000 | Diferencia significativa ✓ |
| Jueves vs Domingo | 0.0000 | Diferencia significativa ✓ |
| Viernes vs Sábado | 0.0119 | Sin diferencia |
| Viernes vs Domingo | 0.0009 | Diferencia significativa ✓ |
| Sábado vs Domingo | 0.2291 | Sin diferencia |

### Conclusión final de la hipótesis

Los días se agrupan en dos comportamientos estadísticamente distintos:

- **Grupo entre semana** (sin diferencia entre sí): Lunes, Martes, Miércoles, Jueves
- **Grupo fin de semana** (sin diferencia entre sí): Viernes, Sábado, Domingo

Todos los días entre semana son significativamente diferentes a todos los días de fin de semana. El viernes ya se comporta estadísticamente como fin de semana, lo que sugiere que el patrón de mayor demanda comienza desde el viernes en la noche.

---

## 4. Modelo de Serie de Tiempo: SARIMA(1,0,0)(1,0,0)[7]

### Paso 1 — Prueba de Estacionariedad: ADF (Augmented Dickey-Fuller)

**¿Por qué esta prueba?**
La estacionariedad es el supuesto fundamental de los modelos ARIMA/SARIMA. Una serie es estacionaria cuando su media y varianza no cambian con el tiempo. Si no fuera estacionaria habría que diferenciarla (parámetro d > 0).

**Supuestos:**
- H0: la serie tiene raíz unitaria (NO es estacionaria)
- H1: la serie ES estacionaria
- Si p < 0.05 se rechaza H0 y se concluye estacionariedad

**Resultado:**

| Estadístico ADF | p-valor | Conclusión |
|----------------|---------|------------|
| -3.5074 | 0.0078 | Serie estacionaria ✅ → d = 0 |

### Paso 2 — Identificación de parámetros: ACF y PACF

**¿Por qué estos gráficos?**
La función de autocorrelación (ACF) y la autocorrelación parcial (PACF) permiten identificar los parámetros p (AR) y q (MA) del modelo, así como detectar estacionalidad.

**Observaciones:**
- La ACF muestra picos significativos cada 7 lags (lag 7, 14, 21...) → estacionalidad semanal confirmada
- La PACF tiene un pico significativo en lag 1 y luego cae → componente AR(1)
- Esto orientó la búsqueda hacia un modelo SARIMA con s=7

### Paso 3 — Selección automática del modelo: auto_arima (criterio AIC)

Se evaluaron múltiples combinaciones de parámetros. El modelo con menor AIC fue seleccionado:

| Modelo | AIC |
|--------|-----|
| ARIMA(0,0,0)(0,0,0)[7] | 10172.37 |
| ARIMA(1,0,0)(0,0,0)[7] | 10013.36 |
| ARIMA(2,0,0)(1,0,0)[7] | 9948.35 |
| **ARIMA(1,0,0)(1,0,0)[7]** | **9935.85 ✓ Mejor** |

### Paso 4 — Diagnóstico del modelo

| Prueba | Valor | Interpretación |
|--------|-------|----------------|
| Ljung-Box | p=0.51 ✅ | Residuos independientes, el modelo captura bien la estructura |
| Jarque-Bera | p=0.00 ⚠️ | Residuos no normales, hay valores atípicos |
| Heterocedasticidad | p=0.00 ⚠️ | Varianza no constante en los residuos |
| Kurtosis | 9.00 ⚠️ | Colas pesadas, confirma presencia de valores extremos |

### Parámetros del modelo final

| Parámetro | Coeficiente | p-valor | Interpretación |
|-----------|-------------|---------|----------------|
| intercepto | 701.27 | 0.000 ✅ | Base de incidentes |
| ar.L1 | 0.3769 | 0.000 ✅ | El valor de hoy depende moderadamente del día anterior |
| ar.S.L7 | 0.3444 | 0.000 ✅ | Efecto estacional semanal significativo |

### Interpretación del modelo
El SARIMA(1,0,0)(1,0,0)[7] es estadísticamente válido y captura correctamente el patrón semanal: las predicciones muestran picos regulares cada 7 días correspondientes a los fines de semana, consistente con los hallazgos de Kruskal-Wallis. Sin embargo, los residuos con kurtosis alta y varianza no constante indican que eventos atípicos como festividades o eventos masivos generan variaciones que el modelo no puede anticipar.

---

## 5. ¿Se puede predecir?

Aunque el modelo SARIMA identifica patrones claros como el aumento de incidentes los fines de semana y en diciembre, consideramos que una predicción precisa es difícil debido a variables externas como días sin carro, eventos masivos o partidos de fútbol, que generan picos atípicos que un modelo basado solo en fechas no podría anticipar. El intervalo de confianza amplio del modelo y la kurtosis elevada de los residuos confirman estadísticamente esta limitación. Para mejorar la predicción sería necesario incorporar estas variables externas al modelo.

---

## Gráficos generados

| Archivo | Descripción |
|---------|-------------|
| `grafico_dias.png` | Promedio de incidentes por día de la semana |
| `grafico_meses.png` | Promedio de incidentes por mes |
| `grafico_boxplot.png` | Distribución y valores atípicos |
| `grafico_anual.png` | Comparación 2022 vs 2023 |
| `grafico_densidad.png` | Distribución por día (verificación supuesto Kruskal-Wallis) |
| `grafico_acf_pacf.png` | ACF y PACF (identificación parámetros SARIMA) |
| `grafico_sarima.png` | Serie de tiempo + predicción 30 días |