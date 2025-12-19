import streamlit as st
from filters import top_10_highest, top_10_lowest, top_10_balanced
from plots import plot_top_heroes, plot_hero_radar

# --- DICCIONARIO DE TRADUCCIÓN ---
# Mapea las claves de la API a español para mostrar en UI y Gráficos
TRADUCCIONES = {
    "intelligence": "Inteligencia",
    "strength": "Fuerza",
    "speed": "Velocidad",
    "durability": "Durabilidad",
    "power": "Poder",
    "combat": "Combate"
}

# --- GESTIÓN DE ESTADO ---
def init_state():
    if "selected_hero" not in st.session_state:
        st.session_state.selected_hero = None
    if "view" not in st.session_state:
        st.session_state.view = "menu"

def change_view(view_name, hero=None):
    st.session_state.view = view_name
    if hero:
        st.session_state.selected_hero = hero

# --- ESTILOS CSS PERSONALIZADOS ---
def render_header():
    st.markdown("""
        <style>
        .main-title {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-weight: 800;
            font-size: 5rem;
            color: #FFFFFF;
            margin-bottom: 0px;
            letter-spacing: +2px;
        }
        .subtitle {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 1.5rem;
            color: #CCCCCC;
            margin-bottom: 30px;
        }
        </style>
        <div class="main-title">Marvel on Your Desk</div>
        <div class="subtitle">Exploración interactiva de héroes</div>
        """, unsafe_allow_html=True)

# --- VISTAS ---

def render_menu(heroes):
    # Buscador Global
    st.markdown("### 🔍 Buscar héroe")
    hero_names = [h.name for h in heroes]
    
    selected_name = st.selectbox(
        "Escribe o selecciona un héroe",
        [""] + hero_names,
        key="search_box",
        label_visibility="collapsed"
    )
    
    if selected_name:
        hero = next(h for h in heroes if h.name == selected_name)
        change_view("hero", hero)
        st.rerun()

    st.divider()

    # Filtros
    col_filter_1, col_filter_2 = st.columns(2)
    
    with col_filter_1:
        # Usamos las claves en inglés para la lógica, pero mostramos español
        stat_key = st.selectbox(
            "Selecciona una estadística",
            options=list(TRADUCCIONES.keys()),
            format_func=lambda x: TRADUCCIONES[x] # Muestra "Inteligencia" en vez de "intelligence"
        )
    
    with col_filter_2:
        ranking_type = st.radio(
            "Tipo de ranking",
            ["Más fuertes", "Más débiles", "Más balanceados"],
            horizontal=True
        )

    # Lógica de obtención de datos (usa key en inglés)
    if ranking_type == "Más fuertes":
        ranking = top_10_highest(heroes, stat_key)
        prefix_title = "Top 10 superior -"
    elif ranking_type == "Más débiles":
        ranking = top_10_lowest(heroes, stat_key)
        prefix_title = "Top 10 inferior -"
    else:
        ranking = top_10_balanced(heroes, stat_key)
        prefix_title = "Top 10 balanceado -"

    # Título de sección en Español
    stat_espanol = TRADUCCIONES[stat_key]
    st.subheader(f"🏆 {prefix_title} {stat_espanol}")

    with st.container():
        # Pasamos stat_label para que el gráfico use el nombre en español
        fig = plot_top_heroes(
            ranking,
            stat=stat_key,
            title_prefix=prefix_title,
            stat_label=stat_espanol 
        )
        if fig:
            st.pyplot(fig, use_container_width=True)

        st.markdown("### Detalle del Ranking")
        
        for i, hero in enumerate(ranking, start=1):
            c1, c2 = st.columns([0.5, 6]) 
            with c1:
                st.markdown(f"**#{i}**")
            with c2:
                st.button(
                    f"{hero.name}", 
                    key=f"btn_{hero.id}_{stat_key}", 
                    on_click=change_view,
                    args=("hero", hero),
                    use_container_width=True
                )


def render_hero_detail():
    hero = st.session_state.selected_hero
    
    st.button("⬅ Volver al menú", on_click=change_view, args=("menu",))

    if not hero:
        st.error("No se ha seleccionado ningún héroe.")
        return

    st.title(hero.name.upper())

    col_info, col_radar = st.columns([1.2, 1])

    with col_info:
        st.markdown("### 📝 Datos Biográficos")
        st.markdown(f"""
        - **Nombre Real:** {hero.full_name or "Desconocido"}
        - **Ocupación:** {hero.occupation or "No registrada"}
        - **Imagen oficial:** [Ver en nueva pestaña ↗]({hero.image_url})
        """)
        
        st.markdown("### 📊 Estadísticas Base")
        s_cols = st.columns(3)
        
        # Iteramos y traducimos las etiquetas
        for idx, (k, v) in enumerate(hero.powerstats.items()):
            label_es = TRADUCCIONES.get(k, k.capitalize()) # Traduce o usa la original
            with s_cols[idx % 3]:
                st.metric(label=label_es, value=v)

        st.divider()
        
        st.markdown("""
        <div style="background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
            <p style="margin:0; font-style: italic;">
            "¿Esa foto oficial te parece aburrida? A mí también. 😏<br>
            Vamos a darle un giro creativo con IA. Pulsa el botón de abajo y prepárate para ver a tu héroe favorito como nunca antes lo habías imaginado."
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("") 
        
        st.button(
            "✨ ¡Reimaginar con IA!", 
            on_click=change_view, 
            args=("ai_image",),
            type="primary",
            use_container_width=True
        )

    with col_radar:
        st.markdown("<br>", unsafe_allow_html=True)
        # El radar tomará las etiquetas en inglés del objeto hero, 
        # pero podemos modificar plot_hero_radar si quisieras traducirlas también allí.
        # Por ahora, renderizará las keys del objeto.
        radar_fig = plot_hero_radar(hero)
        if radar_fig:
            st.pyplot(radar_fig, use_container_width=True)


def render_ai_view():
    hero = st.session_state.selected_hero
    
    st.button("⬅ Volver a ficha del héroe", on_click=change_view, args=("hero",))
    
    st.header(f"🎨 Laboratorio Creativo: {hero.name}")
    
    st.info("🚧 Módulo de DALL·E en construcción...")
    st.markdown(
        f"""
        Estás a un paso de generar una variante única de **{hero.name}**.
        
        En la versión final, aquí verás:
        1. El prompt de generación optimizado.
        2. La imagen generada en estilo Cómic/Dark.
        """
    )

# --- APP RUN ---
def run_ui(heroes):
    st.set_page_config(
        page_title="Marvel Stats",
        page_icon="🛡️",
        layout="wide"
    )

    init_state()
    render_header() 

    if st.session_state.view == "menu":
        render_menu(heroes)
    elif st.session_state.view == "hero":
        render_hero_detail()
    elif st.session_state.view == "ai_image":
        render_ai_view()