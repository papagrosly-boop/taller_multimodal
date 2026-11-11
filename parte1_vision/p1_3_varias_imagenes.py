"""1.3 Varias imágenes (2 o 3) relacionadas en una misma solicitud.
Uso: python parte1_vision/p1_3_varias_imagenes.py [img1 img2 [img3]]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import DIR_IMAGENES, cliente, guardar, listar_imagenes, preguntar_con_imagenes

PREGUNTA = ("Estas imágenes están relacionadas. Compáralas: indica qué tienen en común, "
            "en qué se diferencian y haz un resumen conjunto de los datos más importantes.")


def main():
    if len(sys.argv) > 2:
        rutas = [Path(a) if Path(a).exists() else DIR_IMAGENES / a for a in sys.argv[1:4]]
    else:
        rutas = listar_imagenes()[:3]
    if len(rutas) < 2:
        sys.exit("Necesitas al menos 2 imágenes.")
    respuesta = preguntar_con_imagenes(cliente(), rutas, PREGUNTA)
    salida = f"IMÁGENES: {', '.join(r.name for r in rutas)}\n\nPREGUNTA:\n{PREGUNTA}\n\nRESPUESTA:\n{respuesta}\n"
    print(salida)
    guardar("1_3_respuesta.md", salida)


if __name__ == "__main__":
    main()
