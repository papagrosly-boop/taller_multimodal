"""Esquema de extracción (6 campos) para figuras y tablas de la documentación de TOGAF 9.1.
Útil para Ragi: saber qué es el elemento, de dónde viene (derechos de autor), en qué idioma está
y qué tan complejo es antes de indexarlo en un corpus RAG.
"""
from typing import Optional

from pydantic import BaseModel, ConfigDict

# (campo, tipo, descripción) -> también sirve para llenar la tabla "Esquema" del informe
CAMPOS = [
    ("titulo", "string", "Título principal visible en la imagen; null si la imagen no tiene título"),
    ("numero_figura", "string", "Número de figura o tabla tal como aparece (ej. Figure 5-1); null si no aparece"),
    ("tipo_elemento", "string", "Exactamente uno de: diagrama, tabla"),
    ("idioma", "string", "Idioma del texto de la imagen: español o inglés"),
    ("derechos_autor", "string", "Texto de derechos de autor visible (ej. © The Open Group); null si no hay"),
    ("cantidad_bloques", "integer", "Número de bloques, círculos o componentes de primer nivel (sin contar encabezados ni flechas); solo el número"),
]


class Extraccion(BaseModel):
    """Todos los campos son obligatorios, pero pueden ser null si no se leen en la imagen."""
    model_config = ConfigDict(extra="forbid")

    titulo: Optional[str]
    numero_figura: Optional[str]
    tipo_elemento: Optional[str]
    idioma: Optional[str]
    derechos_autor: Optional[str]
    cantidad_bloques: Optional[int]
