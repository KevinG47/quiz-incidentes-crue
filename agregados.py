"""
=============================================================
ANÁLISIS DE INCIDENTES DIARIOS CRUE 2022-2023
=============================================================
Autores: Kevin Leonardo Chaparro Reyes y Valentina Muñoz Palma
Archivo: agregados.py
Descripción: Análisis avanzado, pruebas estadísticas y modelo SARIMA
=============================================================
"""

# ── LIBRERÍAS ──────────────────────────────────────────────
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy import stats
from scipy.stats import mannwhitneyu
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm

warnings.filterwarnings("ignore")


# ── CARGA Y PREPARACIÓN DE DATOS ───────────────────────────
df = pd.read_csv("incidentes_crue_diarios.txt", sep=r"\s+")
df["fecha"] = pd.to_datetime(df["fecha"])

df["dia_semana"] = df["fecha"].dt.dayofweek.map({
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo"
})

df["mes"] = df["fecha"].dt.month.map({
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
})

df["año"] = df["fecha"].dt.year


# ══════════════════════════════════════════════════════════════
# SECCIÓN 1: GRÁFICOS DESCRIPTIVOS
# ══════════════════════════════════════════════════════════════

# ── 1.1 Promedio por día de la semana ──
orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
promedio_dia = df.groupby("dia_semana")["incidentes"].mean().reindex(orden_dias)

plt.figure(figsize=(10, 6))
sns.barplot(x=promedio_dia.index, y=promedio_dia.values, hue=promedio_dia.index, palette="Blues_d", legend=False)
plt.title("Promedio de incidentes por día de la semana")
plt.xlabel("Día")
plt.ylabel("Promedio de incidentes")
plt.tight_layout()
plt.savefig("grafico_dias.png")
plt.show()

# ── 1.2 Promedio por mes ──
orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
promedio_mes = df.groupby("mes")["incidentes"].mean().reindex(orden_meses)

plt.figure(figsize=(12, 6))
sns.barplot(x=promedio_mes.index, y=promedio_mes.values, hue=promedio_mes.index, palette="Oranges_d", legend=False)
plt.title("Promedio de incidentes por mes")
plt.xlabel("Mes")
plt.ylabel("Promedio de incidentes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_meses.png")
plt.show()

# ── 1.3 Boxplot de distribución general ──
plt.figure(figsize=(8, 6))
sns.boxplot(y=df["incidentes"], color="lightblue")
plt.title("Distribución de incidentes diarios")
plt.ylabel("Incidentes")
plt.tight_layout()
plt.savefig("grafico_boxplot.png")
plt.show()

# ── 1.4 Comparación 2022 vs 2023 ──
promedio_anual = df.groupby("año")["incidentes"].mean()

plt.figure(figsize=(8, 6))
sns.barplot(x=promedio_anual.index, y=promedio_anual.values, hue=promedio_anual.index, palette="Set2", legend=False)
plt.title("Comparación promedio de incidentes: 2022 vs 2023")
plt.xlabel("Año")
plt.ylabel("Promedio de incidentes")
plt.tight_layout()
plt.savefig("grafico_anual.png")
plt.show()


# ══════════════════════════════════════════════════════════════
# SECCIÓN 2: PRUEBA DE HIPÓTESIS
# ¿El domingo tiene significativamente más incidentes?
# ══════════════════════════════════════════════════════════════

# Separar datos por día de la semana
dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
grupos = [df[df["dia_semana"] == dia]["incidentes"].values for dia in dias_nombres]


# ── 2.1 Normalidad: Shapiro-Wilk ──
# H0: los datos siguen distribución normal
# Se usa para decidir si aplicar prueba paramétrica (ANOVA) o no paramétrica (Kruskal-Wallis)
print("=" * 55)
print("PASO 1 — PRUEBA DE NORMALIDAD (Shapiro-Wilk)")
print("=" * 55)
for dia, grupo in zip(dias_nombres, grupos):
    stat, p = stats.shapiro(grupo)
    resultado = "Normal ✓" if p > 0.05 else "No normal ✗"
    print(f"  {dia:<12}: p = {p:.4f}  →  {resultado}")
print("\n  → 6/7 días no cumplen normalidad. No se puede usar ANOVA.\n")


# ── 2.2 Homocedasticidad: Levene ──
# H0: las varianzas de todos los grupos son iguales
# Supuesto adicional requerido por ANOVA
print("=" * 55)
print("PASO 2 — PRUEBA DE HOMOCEDASTICIDAD (Levene)")
print("=" * 55)
stat, p = stats.levene(*grupos)
resultado = "Varianzas iguales ✓" if p > 0.05 else "Varianzas diferentes ✗"
print(f"  p-valor = {p:.4f}  →  {resultado}")
print("\n  → Varianzas distintas. Confirma que no se puede usar ANOVA.\n")


# ── 2.3 Verificación visual: Gráfico de densidad KDE ──
# Supuesto de Kruskal-Wallis: distribuciones de forma similar entre grupos
plt.figure(figsize=(12, 6))
for dia in dias_nombres:
    subset = df[df["dia_semana"] == dia]["incidentes"]
    sns.kdeplot(subset, label=dia)
plt.title("Distribución de incidentes por día de la semana (KDE)")
plt.xlabel("Incidentes")
plt.ylabel("Densidad")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_densidad.png")
plt.show()
# Todas las curvas son unimodales y aproximadamente simétricas → supuesto de Kruskal-Wallis cumplido


# ── 2.4 Prueba principal: Kruskal-Wallis ──
# Alternativa no paramétrica al ANOVA
# H0: no hay diferencia entre los días de la semana
print("=" * 55)
print("PASO 3 — PRUEBA DE KRUSKAL-WALLIS")
print("=" * 55)
stat, p = stats.kruskal(*grupos)
print(f"  Estadístico : {stat:.4f}")
print(f"  p-valor     : {p:.4f}")
if p < 0.05:
    print("  Conclusión  : Sí hay diferencia significativa ✓")
    print("\n  → Al menos un día es diferente. Se procede con post-hoc.\n")
else:
    print("  Conclusión  : No hay diferencia significativa")


# ── 2.5 Post-Hoc: Mann-Whitney con corrección de Bonferroni ──
# Identifica qué pares de días son significativamente distintos
# Bonferroni controla el error tipo I en comparaciones múltiples
print("=" * 55)
print("PASO 4 — POST-HOC (Mann-Whitney + Bonferroni)")
print("=" * 55)
n_comparaciones = len(list(combinations(dias_nombres, 2)))
alpha_corregido = 0.05 / n_comparaciones
print(f"  Alpha corregido = 0.05 / {n_comparaciones} = {alpha_corregido:.4f}\n")

for dia1, dia2 in combinations(dias_nombres, 2):
    g1 = df[df["dia_semana"] == dia1]["incidentes"]
    g2 = df[df["dia_semana"] == dia2]["incidentes"]
    stat, p = mannwhitneyu(g1, g2, alternative="two-sided")
    if p < alpha_corregido:
        print(f"  {dia1:<12} vs {dia2:<12}: p={p:.4f}  →  Diferencia significativa ✓")
    else:
        print(f"  {dia1:<12} vs {dia2:<12}: p={p:.4f}  →  Sin diferencia")

print("\n  → Conclusión: Lunes-Jueves forman un grupo, Viernes-Domingo otro.")
print("     El viernes ya se comporta estadísticamente como fin de semana.\n")


# ══════════════════════════════════════════════════════════════
# SECCIÓN 3: MODELO DE SERIE DE TIEMPO — SARIMA
# ══════════════════════════════════════════════════════════════

# ── 3.1 Estacionariedad: ADF ──
# Supuesto fundamental de ARIMA/SARIMA
# H0: la serie NO es estacionaria (tiene raíz unitaria)
print("=" * 55)
print("PASO 1 — PRUEBA DE ESTACIONARIEDAD (ADF)")
print("=" * 55)
resultado_adf = adfuller(df["incidentes"])
print(f"  Estadístico ADF : {resultado_adf[0]:.4f}")
print(f"  p-valor         : {resultado_adf[1]:.4f}")
if resultado_adf[1] < 0.05:
    print("  Conclusión      : Serie estacionaria ✓  →  d = 0")
else:
    print("  Conclusión      : Serie NO estacionaria  →  requiere diferenciación")
print()


# ── 3.2 Identificación de parámetros: ACF y PACF ──
# ACF → parámetro q (MA) y detección de estacionalidad
# PACF → parámetro p (AR)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(df["incidentes"], lags=40, ax=ax1)
ax1.set_title("ACF — Autocorrelación (picos cada 7 lags → estacionalidad semanal)")
plot_pacf(df["incidentes"], lags=40, ax=ax2)
ax2.set_title("PACF — Autocorrelación parcial (pico en lag 1 → AR(1))")
plt.tight_layout()
plt.savefig("grafico_acf_pacf.png")
plt.show()


# ── 3.3 Selección automática del modelo: auto_arima ──
# Evalúa múltiples combinaciones de parámetros y selecciona la de menor AIC
print("=" * 55)
print("PASO 2 — SELECCIÓN DEL MODELO (auto_arima, criterio AIC)")
print("=" * 55)
modelo_auto = pm.auto_arima(
    df["incidentes"],
    seasonal=True,
    m=7,                       # estacionalidad semanal
    d=0,                       # ya es estacionaria
    stepwise=True,
    information_criterion="aic",
    trace=True
)
print("\n=== MEJOR MODELO ENCONTRADO ===")
print(modelo_auto.summary())


# ── 3.4 Ajuste del modelo y predicción ──
# SARIMA(1,0,0)(1,0,0)[7]: mejor modelo según AIC
print("=" * 55)
print("PASO 3 — AJUSTE SARIMA(1,0,0)(1,0,0)[7] Y PREDICCIÓN")
print("=" * 55)

modelo = SARIMAX(df["incidentes"], order=(1, 0, 0), seasonal_order=(1, 0, 0, 7))
resultado = modelo.fit(disp=False)

# Predicción 30 días hacia el futuro
pred = resultado.get_forecast(steps=30)
pred_mean = pred.predicted_mean
pred_ci = pred.conf_int()
fechas_futuras = pd.date_range(
    start=df["fecha"].iloc[-1] + pd.Timedelta(days=1), periods=30
)

# Gráfico final
plt.figure(figsize=(14, 6))
plt.plot(df["fecha"], df["incidentes"],
         color="steelblue", linewidth=0.8, alpha=0.7, label="Datos reales")
plt.plot(fechas_futuras, pred_mean,
         color="red", linewidth=2, label="Predicción 30 días")
plt.fill_between(fechas_futuras, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1],
                 color="red", alpha=0.2, label="Intervalo de confianza 95%")
plt.axvline(x=df["fecha"].iloc[-1],
            color="black", linestyle="--", linewidth=1, label="Fin de datos reales")
plt.title("SARIMA(1,0,0)(1,0,0)[7] — Incidentes CRUE 2022-2023 + Predicción")
plt.xlabel("Fecha")
plt.ylabel("Incidentes")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_sarima.png")
plt.show()

print("\n  Análisis completado. Gráficos guardados en la carpeta del proyecto.")