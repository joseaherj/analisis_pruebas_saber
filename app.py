import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import skew

import matplotlib as mpl
mpl.rcParams['axes.labelsize']= 22
mpl.rcParams['legend.fontsize']= 15
mpl.rcParams['xtick.major.size']= 16
mpl.rcParams['xtick.minor.size']= 8
mpl.rcParams['ytick.major.size']= 16
mpl.rcParams['ytick.minor.size']= 8
mpl.rcParams['xtick.labelsize']= 16
mpl.rcParams['ytick.labelsize']= 16

# Load data
df = pd.read_csv("saber_11.csv")

# Areas/modules to analyze
modules = [
    "LECTURA CRÍTICA",
    "MATEMATICAS",
    "INGLÉS",
    "GLOBAL"
]

df2  = pd.read_csv("saber_pro.csv")
modules_pro = [
 'LECTURA CRÍTICA',
 'RAZONAMIENTO CUANTITATIVO',
 'INGLÉS',
 'GLOBAL',
 ]

col1, col2 = st.columns(2)

with col1:

    st.title("Análisis de Puntajes por Área de Saber 11")

    # Select module
    selected_module = st.selectbox("Seleccione un módulo:", modules)

    # Get scores
    scores = df[selected_module].dropna()

    scores = scores.apply(pd.to_numeric, errors='coerce')

    # Compute stats
    mean_score = np.nanmean(scores)
    median_score = np.nanmedian(scores)
    clean_data = scores[~np.isnan(scores)]
    skewness_score = skew(clean_data)
    min_score = scores.min()
    max_score = scores.max()

    # Show stats
    st.markdown(f"**Media:** {mean_score:.2f}")
    st.markdown(f"**Mediana:** {median_score:.2f}")
    st.markdown(f"**Asimetría (Skewness):** {skewness_score:.2f}")
    st.markdown(f"**Mínimo:** {min_score:.0f}")
    st.markdown(f"**Máximo:** {max_score:.0f}")

    # Plot histogram + KDE
    fig, ax = plt.subplots()
    sns.histplot(scores, kde=True, ax=ax, bins=10)
    ax.axvline(mean_score, color='r', linestyle='--', label=f'Media: {mean_score:.2f}')
    ax.axvline(median_score, color='g', linestyle=':', label=f'Mediana: {median_score:.2f}')
    ax.set_title(f"Distribución de puntajes: {selected_module}", fontsize=20)
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    # Show plot
    st.pyplot(fig)

with col2:    
    st.title("Análisis de Puntajes por Área de Saber Pro")

    # Select module
    selected_module_pro = st.selectbox("Seleccione un módulo:", modules_pro)

    # Get scores
    scores_pro = df2[selected_module_pro].dropna()
    
    scores_pro = scores_pro.apply(pd.to_numeric, errors='coerce')

    # Compute stats
    mean_score_pro = np.nanmean(scores_pro)
    median_score_pro = np.nanmedian(scores_pro)
    clean_data = scores_pro[~np.isnan(scores_pro)]
    skewness_score_pro = skew(clean_data)
    min_score_pro = scores_pro.min()
    max_score_pro = scores_pro.max()

    # Show stats
    st.markdown(f"**Media:** {mean_score_pro:.2f}")
    st.markdown(f"**Mediana:** {median_score_pro:.2f}")
    st.markdown(f"**Asimetría (Skewness):** {skewness_score_pro:.2f}")
    st.markdown(f"**Mínimo:** {min_score_pro:.0f}")
    st.markdown(f"**Máximo:** {max_score_pro:.0f}")

    # Plot histogram + KDE
    fig, ax = plt.subplots()
    sns.histplot(scores_pro, kde=True, ax=ax, bins=10)
    ax.axvline(mean_score_pro, color='r', linestyle='--', label=f'Media: {mean_score_pro:.2f}')
    ax.axvline(median_score_pro, color='g', linestyle=':', label=f'Mediana: {median_score_pro:.2f}')
    ax.set_title(f"Distribución de puntajes: {selected_module_pro}", fontsize=20)
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    # Show plot
    st.pyplot(fig)

st.title("Comparación resultados Saber 11 vs Saber Pro")

merged_df = pd.read_csv("merged_tab.csv")

# Pares para comparar
comparison_pairs = [
    ("MATEMÁTICAS", merged_df['MATEMATICAS'], 
     "RAZONAMIENTO CUANTITATIVO", merged_df['RAZONAMIENTO CUANTITATIVO']),
    
    ("LECTURA CRÍTICA", merged_df['LECTURA CRÍTICA_1'], 
     "LECTURA CRÍTICA", merged_df['LECTURA CRÍTICA_2']),
    
    ("INGLÉS", merged_df['INGLÉS_1'], 
     "INGLÉS", merged_df['INGLÉS_2']),
    
    ("PUNTAJE GLOBAL", merged_df['GLOBAL_1'], 
     "PUNTAJE GLOBAL", merged_df['GLOBAL_2']),
]

# Crear figura tipo mosaico 2x2
fig, axs = plt.subplots(2, 2, figsize=(18, 18))
axs = axs.flatten()

# Dibujar los gráficos con líneas guía
for i, (label1, x_vals, label2, y_vals) in enumerate(comparison_pairs):
    ax = axs[i]
    ax.scatter(x_vals, y_vals, alpha=0.6, s=150, edgecolor='black')
    if i==3:
        ax.axvline(250, color='gray', linestyle='--', label='Línea vertical: 250')
        ax.axhline(150, color='red', linestyle='--', label='Línea horizontal: 150')
    else:
        ax.axvline(50, color='gray', linestyle='--', label='Línea vertical: 50')
        ax.axhline(150, color='red', linestyle='--', label='Línea horizontal: 150')
    ax.set_xlabel(f'{label1} (Saber 11)', color='blue')
    ax.set_ylabel(f'{label2} (Saber Pro)', color='red')
    #ax.set_title(f'{label1} vs {label2}', fontsize=20)
    ax.legend()
    ax.grid(True)

# Mostrar en Streamlit
st.pyplot(fig)
