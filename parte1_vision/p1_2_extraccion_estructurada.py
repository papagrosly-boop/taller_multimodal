"""1.2 Extracción estructurada en JSON de 3 imágenes + validación + % de aciertos.
Requiere imagenes/valores_reales.json (lo que TÚ lees en cada imagen).
Uso: python parte1_vision/p1_2_extraccion_estructurada.py [img1 img2 img3]
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pydantic import ValidationError

from common import DIR_IMAGENES, DIR_RESULTADOS, cliente, listar_imagenes, preguntar_con_imagenes
from schema import CAMPOS, Extraccion

REALES = DIR_IMAGENES / "valores_reales.json"


def crear_plantilla_reales(nombres):
    plantilla = {n: {c: "" for c, _, _ in CAMPOS} for n in nombres}
    REALES.write_text(json.dumps(plantilla, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.exit(f"Creé {REALES.name} con una plantilla. Llena los valores REALES que lees en cada "
             "imagen (usa null si no aparece) y vuelve a ejecutar.")


def prompt() -> str:
    lista = "\n".join(f"- {c}: {d}" for c, _, d in CAMPOS)
    return ("Extrae de la imagen los siguientes campos y responde ÚNICAMENTE con un objeto JSON "
            "válido, sin texto adicional ni bloques de código. Usa null si un campo no aparece "
            f"o no se lee. Campos:\n{lista}")


def extraer_json(texto: str):
    m = re.search(r"\{.*\}", texto, flags=re.S)
    return json.loads(m.group(0) if m else texto)


def norm(v) -> str:
    return re.sub(r"[^a-z0-9]", "", str(v if v is not None else "").lower())


def main():
    args = sys.argv[1:4]
    rutas = [Path(a) if Path(a).exists() else DIR_IMAGENES / a for a in args] or listar_imagenes()[:3]
    if len(rutas) < 3:
        sys.exit("Necesitas 3 imágenes en imagenes/ (o pásalas como argumentos).")
    if not REALES.exists():
        crear_plantilla_reales([r.name for r in rutas])
    reales = json.loads(REALES.read_text(encoding="utf-8"))

    client = cliente()
    filas, aciertos, total = [], 0, 0
    for ruta in rutas:
        print(f"\n=== {ruta.name} ===")
        crudo = preguntar_con_imagenes(client, [ruta], prompt())
        print("Respuesta cruda:", crudo)
        try:
            datos = Extraccion.model_validate(extraer_json(crudo)).model_dump()
            print("JSON válido según el esquema.")
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"[AVISO] La salida NO cumple el esquema: {str(e)[:300]}")
            datos = {}
        real = reales.get(ruta.name, {})
        for campo, _, _ in CAMPOS:
            v_real, v_ext = real.get(campo), datos.get(campo)
            ok = norm(v_real) == norm(v_ext)
            total += 1
            aciertos += ok
            filas.append([ruta.name, campo, v_real, v_ext, "Sí" if ok else "No"])

    pct = 100 * aciertos / total if total else 0
    with open(DIR_RESULTADOS / "1_2_tabla_aciertos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["imagen", "campo", "valor_real", "valor_extraido", "correcto"])
        w.writerows(filas)
    print("\n" + "-" * 70)
    for fila in filas:
        print(" | ".join(str(x) for x in fila))
    print(f"\nPorcentaje de aciertos: {aciertos} de {total} campos = {pct:.1f} %")


if __name__ == "__main__":
    main()
