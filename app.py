import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew

# Load data
df = pd.read_csv("saber_11.csv")

# Areas/modules to analyze
modules = [
    "LECTURA CRÍTICA",
    "MATEMÁTICAS",
    "SOCIALES Y CIUDADANAS",
    "CIENCIAS NATURALES",
    "INGLÉS"
]

df["PUNTAJE GLOBAL"] = df[modules].sum(axis=1)

modules.append("PUNTAJE GLOBAL")


df2  = pd.read_csv("saber_pro.csv")
modules_pro = [
 'LECTURA CRÍTICA',
 'INGLÉS',
 'COMPETENCIAS CIUDADANAS',
 'COMUNICACIÓN ESCRITA',
 'RAZONAMIENTO CUANTITATIVO']


df2["PUNTAJE GLOBAL"] = df2[modules_pro].sum(axis=1)

modules_pro.append("PUNTAJE GLOBAL")


col1, col2 = st.columns(2)

with col1:

    st.title("Análisis de Puntajes por Módulo de Saber 11")

    # Select module
    selected_module = st.selectbox("Seleccione un módulo:", modules)

    # Get scores
    scores = df[selected_module].dropna()

    # Compute stats
    mean_score = scores.mean()
    median_score = scores.median()
    skewness_score = skew(scores)
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
    ax.set_title(f"Distribución de puntajes: {selected_module}")
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    # Show plot
    st.pyplot(fig)

with col2:    
    st.title("Análisis de Puntajes por Módulo de Saber Pro")

    # Select module
    selected_module_pro = st.selectbox("Seleccione un módulo:", modules_pro)

    # Get scores
    scores_pro = df2[selected_module_pro].dropna()

    # Compute stats
    mean_score_pro = scores_pro.mean()
    median_score_pro = scores_pro.median()
    skewness_score_pro = skew(scores_pro)
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
    ax.set_title(f"Distribución de puntajes: {selected_module_pro}")
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("Frecuencia")
    ax.legend()

    # Show plot
    st.pyplot(fig)

merged_df = pd.read_csv("merged_tab.csv")

# Calcular GLOBAL para ambos
merged_df["GLOBAL_1"] = merged_df[['LECTURA CRÍTICA_1', 'MATEMÁTICAS', 'SOCIALES Y CIUDADANAS', 'CIENCIAS NATURALES', 'INGLÉS_1']].mean(axis=1)
merged_df["GLOBAL_2"] = merged_df[['LECTURA CRÍTICA_2', 'INGLÉS_2', 'COMPETENCIAS CIUDADANAS', 'COMUNICACIÓN ESCRITA', 'RAZONAMIENTO CUANTITATIVO']].mean(axis=1)

# Promedio entre matemáticas y ciencias naturales
merged_df["MAT_CIEN_1"] = merged_df[['MATEMÁTICAS', 'CIENCIAS NATURALES']].mean(axis=1)

# Pares para comparar
comparison_pairs = [
    ("Prom. MATEMÁTICAS y CIENCIAS NATURALES", merged_df['MAT_CIEN_1'], 
     "RAZONAMIENTO CUANTITATIVO", merged_df['RAZONAMIENTO CUANTITATIVO']),
    
    ("LECTURA CRÍTICA_1", merged_df['LECTURA CRÍTICA_1'], 
     "LECTURA CRÍTICA_2", merged_df['LECTURA CRÍTICA_2']),
    
    ("SOCIALES Y CIUDADANAS", merged_df['SOCIALES Y CIUDADANAS'], 
     "COMPETENCIAS CIUDADANAS", merged_df['COMPETENCIAS CIUDADANAS']),
    
    ("INGLÉS_1", merged_df['INGLÉS_1'], 
     "INGLÉS_2", merged_df['INGLÉS_2']),
    
    ("GLOBAL_1", merged_df['GLOBAL_1'], 
     "GLOBAL_2", merged_df['GLOBAL_2']),
]

# Crear figura tipo mosaico 3x2
fig, axs = plt.subplots(3, 2, figsize=(14, 18))
axs = axs.flatten()

# Dibujar los gráficos con líneas guía
for i, (label1, x_vals, label2, y_vals) in enumerate(comparison_pairs):
    ax = axs[i]
    ax.scatter(x_vals, y_vals, alpha=0.6)
    ax.axvline(50, color='gray', linestyle='--', label='Línea vertical: 50')
    ax.axhline(150, color='red', linestyle='--', label='Línea horizontal: 150')
    ax.set_xlabel(f'{label1} (Saber 11)')
    ax.set_ylabel(f'{label2} (Saber Pro)')
    ax.set_title(f'{label1} vs {label2}')
    ax.legend()
    ax.grid(True)

# Quitar subplot sobrante si hay menos de 6
if len(comparison_pairs) < 6:
    fig.delaxes(axs[-1])

# Mostrar en Streamlit
st.pyplot(fig)
