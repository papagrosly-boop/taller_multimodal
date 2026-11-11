"""1.1 Pregunta sobre una imagen local (base64).
Uso: python parte1_vision/p1_1_pregunta_imagen.py [imagen] ["pregunta"]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import DIR_IMAGENES, cliente, guardar, listar_imagenes, preguntar_con_imagenes

PREGUNTA_POR_DEFECTO = (
    "Esta imagen es una figura o tabla de la documentación de TOGAF 9.1. Explica qué "
    "representa, a qué fase o parte del método ADM corresponde y cuáles son sus elementos "
    "principales. Si algo no se lee con claridad, indícalo."
)  # <- cámbiala por una pregunta propia de tu dominio


def main():
    imagenes = listar_imagenes()
    if not imagenes and len(sys.argv) < 2:
        sys.exit("Pon al menos una imagen en imagenes/ o pásala como argumento.")
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else imagenes[0]
    if not ruta.exists():
        ruta = DIR_IMAGENES / ruta.name
    pregunta = sys.argv[2] if len(sys.argv) > 2 else PREGUNTA_POR_DEFECTO

    respuesta = preguntar_con_imagenes(cliente(), [ruta], pregunta)
    salida = f"IMAGEN: {ruta.name}\n\nPREGUNTA:\n{pregunta}\n\nRESPUESTA:\n{respuesta}\n"
    print(salida)
    guardar("1_1_respuesta.md", salida)


if __name__ == "__main__":
    main()
