# src/filters.py
from typing import List
from models import Hero

def top_10_highest(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Obtiene los 10 héroes con el valor MÁS ALTO en una estadística específica.
    
    Args:
        heroes: Lista de objetos Hero.
        stat: Nombre de la estadística (ej: 'intelligence', 'strength').
    """
    # 1. Filtrado: Solo héroes válidos y que tengan la estadística mayor a 0
    valid = [
        h for h in heroes
        if h.has_valid_stats() and h.powerstats.get(stat, 0) > 0
    ]

    # 2. Ordenamiento Descendente (reverse=True) y corte de los primeros 10
    return sorted(
        valid,
        key=lambda h: h.powerstats[stat],
        reverse=True
    )[:10]


def top_10_lowest(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Obtiene los 10 héroes con el valor MÁS BAJO en una estadística específica.
    Útil para encontrar las debilidades más marcadas.
    """
    valid = [
        h for h in heroes
        if h.has_valid_stats() and h.powerstats.get(stat, 0) > 0
    ]

    # 2. Ordenamiento Ascendente (por defecto) y corte de los primeros 10
    return sorted(
        valid,
        key=lambda h: h.powerstats[stat]
    )[:10]


def top_10_balanced(heroes: List[Hero], stat: str) -> List[Hero]:
    """
    Encuentra los héroes cuyo valor en 'stat' está más cerca de su propio promedio general.
    
    Interpretación:
    Busca héroes consistentes donde esta estadística específica no se aleja
    de su nivel de poder habitual.
    """
    valid = [
        h for h in heroes
        if h.has_valid_stats() and h.powerstats.get(stat, 0) > 0
    ]

    # 2. Ordenamiento por menor desviación (abs) respecto a su promedio
    return sorted(
        valid,
        key=lambda h: abs(h.powerstats[stat] - h.average_power())
    )[:10]