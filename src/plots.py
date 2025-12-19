import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

def _load_comic_font():
    """Carga Comic Sans MS configurada para contraste alto en fondo oscuro."""
    try:
        return font_manager.FontProperties(family="Comic Sans MS")
    except:
        return None

def setup_comic_style(ax, comic_font):
    """Estética de bordes y textos para modo oscuro."""
    # Ocultamos los bordes del cuadro (spines) para que se vea más limpio
    # ya que las barras no tendrán contorno.
    for spine in ax.spines.values():
        spine.set_visible(False) 
    
    # Solo dejamos visible la línea izquierda si quieres una referencia, 
    # si no, lo dejamos todo limpio como se ve en diseños modernos.
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_color('#FFFFFF')
    ax.spines['left'].set_linewidth(1)
    
    if comic_font:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(comic_font)
            label.set_color('#FFFFFF')

# En src/plots.py

def plot_top_heroes(heroes, stat: str, title_prefix: str, stat_label: str = None):
    """
    Ahora acepta 'stat_label' opcional. 
    Si se envía, usa ese nombre en el título (ej: 'Fuerza').
    Si no, usa la stat interna (ej: 'STRENGTH').
    """
    if not heroes: return None

    names = [hero.name.upper() for hero in heroes]
    values = [int(hero.powerstats.get(stat, 0)) for hero in heroes]
    comic_font = _load_comic_font()
    
    # Determinar qué etiqueta usar en el título
    final_stat_name = stat_label if stat_label else stat.upper()

    # --- PALETA ARMÓNICA ---
    colors = ["#FFD54F" if i == 0 else "#FF8A65" if i < 3 else "#90CAF9" for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
    
    fig.patch.set_facecolor('#001435') 
    fig.patch.set_alpha(0.5)
    ax.set_facecolor("none")

    bars = ax.barh(names, values, color=colors, edgecolor=None)
    ax.invert_yaxis()

    # TÍTULO ACTUALIZADO CON LÓGICA DE IDIOMA
    ax.set_title(f"{title_prefix} {final_stat_name}", fontsize=16, 
                 fontproperties=comic_font, weight='bold', color='#FFFFFF', pad=15)
    
    setup_comic_style(ax, comic_font)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width}', 
                va='center', fontproperties=comic_font, weight='bold', 
                fontsize=10, color='#FFFFFF')

    plt.tight_layout()
    return fig

def plot_hero_radar(hero):
    stats = hero.powerstats
    labels = [k.upper() for k in stats.keys()]
    values = [int(v) if v != 'null' else 0 for v in stats.values()]
    if not any(values): return None

    comic_font = _load_comic_font()
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True), dpi=200)

    # Fondo Tarjeta Azul Profundo (#001435)
    fig.patch.set_facecolor("#001435")
    fig.patch.set_alpha(0.8)
    ax.set_facecolor("none")

    # --- ESTILO RADAR ---
    # Línea: Amarillo Paja Suave (#FFF176)
    # Relleno: Mismo amarillo, muy transparente (alpha=0.25)
    ax.plot(angles, values, color="#FFF176", linewidth=1.5, linestyle='solid')
    ax.fill(angles, values, color="#FFF176", alpha=0.25)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Etiquetas
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=6, color='#FFFFFF')
    
    if comic_font:
        for label in ax.get_xticklabels():
            label.set_fontproperties(comic_font)
            label.set_size(6) 
            label.set_color('#FFFFFF')

    ax.set_ylim(0, 100)
    ax.set_yticklabels([])
    
    # --- GRID (Rejilla) ---
    # Gris Claro (#E0E0E0) con opacidad media para que se distinga del fondo oscuro
    ax.grid(True, color="#E0E0E0", linestyle='--', alpha=0.4)
    
    # Color del borde circular exterior (spine polar)
    ax.spines['polar'].set_color('#E0E0E0')
    ax.spines['polar'].set_alpha(0.4)

    ax.set_title(hero.name.upper(), size=10, fontproperties=comic_font, 
                 weight='bold', pad=20, color='#FFFFFF')

    plt.tight_layout()  
    return fig