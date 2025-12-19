# src/app.py
"""
Punto de entrada de la aplicación.
Orquesta la carga de datos y el lanzamiento de la interfaz gráfica.
"""

from pathlib import Path
from loader import load_heroes_from_json
from ui import run_ui


def main():
    # 1. Definición robusta de rutas (independiente del SO)
    base_path = Path(__file__).resolve().parent.parent
    json_path = base_path / "data" / "superheros.json"

    # 2. Carga y filtrado de datos según reglas de negocio (models.py)
    heroes = load_heroes_from_json(json_path)

    # 3. Validación de seguridad (Fail-fast)
    if not heroes:
        raise RuntimeError("No se pudieron cargar héroes válidos. Verifica el JSON o los filtros.")

    # 4. Iniciar la UI de Streamlit
    print(f"✅ Iniciando sistema con {len(heroes)} héroes cargados.")
    run_ui(heroes)


if __name__ == "__main__":
    main()