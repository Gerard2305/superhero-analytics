# src/loader.py
import json
from pathlib import Path
from typing import List

from models import Hero

def load_heroes_from_json(path: str | Path) -> List[Hero]:
    """
    Carga, filtra y transforma datos crudos de JSON a objetos Hero.
    
    Proceso:
    1. Lee el archivo JSON.
    2. Filtra por editorial (Marvel).
    3. Limpia datos numéricos (stats).
    4. Valida reglas de negocio (has_valid_stats).
    """
    json_path = Path(path)

    # 1. Validación de existencia del archivo
    if not json_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    # 2. Lectura del contenido
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # El JSON de la API envuelve la lista dentro de la clave "results"
    data = raw_data.get("results", [])

    heroes: List[Hero] = []

    # 3. Procesamiento y Mapeo
    for item in data:
        try:
            # --- FILTRO 1: Editorial ---
            # Solo procesamos personajes de Marvel Comics
            publisher = item["biography"].get("publisher", "")
            if publisher != "Marvel Comics":
                continue

            # --- SANITIZACIÓN: Powerstats ---
            # Convierte "null" o strings a int. Si falla, asigna 0.
            powerstats = {
                stat: int(value) if str(value).isdigit() else 0
                for stat, value in item["powerstats"].items()
            }

            # --- INSTANCIACIÓN ---
            hero = Hero(
                id=int(item["id"]),
                name=item["name"],
                full_name=item["biography"].get("full-name", ""),
                place_of_birth=item["biography"].get("place-of-birth", ""),
                occupation=item["work"].get("occupation", ""),
                powerstats=powerstats,
                image_url=item["image"].get("url", ""),
            )

            # --- FILTRO 2: Calidad de Datos ---
            # Aplicamos reglas de negocio (sin ceros excesivos, valores > 15, etc.)
            if hero.has_valid_stats():
                heroes.append(hero)

        except (KeyError, ValueError, TypeError):
            # Omitimos registros corruptos sin detener la ejecución
            continue

    return heroes