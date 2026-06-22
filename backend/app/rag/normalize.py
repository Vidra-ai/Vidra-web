"""Normalización de consultas para mejorar la recuperación.

El objetivo es que abreviaturas y variantes tipográficas frecuentes en
documentación corporativa española se conecten con el texto indexado,
tanto en la búsqueda vectorial como en la léxica.
"""

from __future__ import annotations

import re
import unicodedata

# Abreviatura normalizada -> formas canónicas que se añaden a la consulta.
_ABBREVIATIONS: dict[str, list[str]] = {
    "dir": ["direccion", "director"],
    "dira": ["direccion", "director"],
    "dpto": ["departamento"],
    "depto": ["departamento"],
    "dept": ["departamento"],
    "admon": ["administracion"],
    "cia": ["compania"],
    "tlf": ["telefono"],
    "tel": ["telefono"],
    "telf": ["telefono"],
    "ext": ["extension"],
    "num": ["numero"],
    "avda": ["avenida"],
    "avd": ["avenida"],
    "ref": ["referencia"],
    "fra": ["factura"],
    "ctto": ["contrato"],
    "contrat": ["contratacion"],
}


def strip_accents(text: str) -> str:
    """Elimina diacríticos y normaliza caracteres de compatibilidad (ª -> a, º -> o)."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


def _normalize_token(token: str) -> str:
    """Minúsculas, sin acentos y sin puntuación de borde para casar con el diccionario."""
    return strip_accents(token).lower().strip(".,;:()ªº°-/")


def expand_abbreviations(query: str) -> str:
    """Devuelve la consulta original más las formas canónicas de las abreviaturas detectadas."""
    extras: list[str] = []
    seen: set[str] = set()
    for token in re.split(r"\s+", query):
        norm = _normalize_token(token)
        for expansion in _ABBREVIATIONS.get(norm, []):
            if expansion not in seen:
                seen.add(expansion)
                extras.append(expansion)
    if not extras:
        return query
    return f"{query} {' '.join(extras)}"
