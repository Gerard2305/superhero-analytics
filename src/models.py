# src/models.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class Hero:
    id: int
    name: str
    full_name: str
    place_of_birth: str
    occupation: str
    powerstats: Dict[str, int]
    image_url: str

    def has_valid_stats(self) -> bool:
        """
        Filtra héroes basándose en la calidad de sus datos.
        
        Reglas de Negocio:
        1. NO FALTANTES: Excluir si tiene 3 o más estadísticas en 0.
        2. NO OVERPOWERED: Excluir si tiene más de 4 estadísticas en 100.
        3. MÍNIMO HEROICO: Todas las estadísticas deben ser estrictamente mayores a 15.
        """
        values = list(self.powerstats.values())
        
        # Regla 1: Demasiados ceros (datos incompletos)
        if values.count(0) >= 3:
            return False

        # Regla 2: Demasiados cienes (personajes genéricos/rotos)
        if values.count(100) > 4:
            return False

        # Regla 3: Suelo de calidad
        # Si ALGUNA estadística es 15 o menos, el héroe no clasifica.
        # El usuario pidió: "que cualquier estadística sea mayor a 15"
        if any(v <= 15 for v in values):
            return False

        return True

    def average_power(self) -> float:
        """
        Calcula el promedio ignorando ceros técnicos.
        """
        valid_stats = [v for v in self.powerstats.values() if v > 0]
        if not valid_stats:
            return 0.0
        return sum(valid_stats) / len(valid_stats)