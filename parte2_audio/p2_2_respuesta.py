"""2.2 Flujo completo: audio -> transcripción -> respuesta del modelo.
Usa resultados/2_1_transcripciones.csv (ejecuta antes p2_1_transcripcion.py).
Uso: python parte2_audio/p2_2_respuesta.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import DIR_RESULTADOS, DOMINIO, MODELO_TEXTO, cliente, limpiar

SISTEMA = (f"Eres Ragi, un asistente académico experto exclusivamente en {DOMINIO} "
           "(método ADM, arquitectura de negocio, de datos, de aplicaciones y de tecnología, y principios). "
           "Responde en español, de forma clara y precisa. Si la consulta es ajena a TOGAF 9.1, "
           "recházala con transparencia y explica que solo respondes sobre ese marco. "
           "Si la pregunta es ambigua o parece mal transcrita, dilo.")


def main():
    entrada = DIR_RESULTADOS / "2_1_transcripciones.csv"
    if not entrada.exists():
        sys.exit("Primero ejecuta parte2_audio/p2_1_transcripcion.py")
    client, salida = cliente(), []
    with open(entrada, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            r = client.chat.completions.create(
                model=MODELO_TEXTO, temperature=0.2, max_tokens=600,
                messages=[{"role": "system", "content": SISTEMA},
                          {"role": "user", "content": fila["transcripcion"]}])
            resp = limpiar(r.choices[0].message.content)
            print(f"\n[{fila['archivo']}]\nAUDIO -> {fila['transcripcion']}\nRESPUESTA -> {resp}")
            salida.append({"archivo": fila["archivo"], "transcripcion": fila["transcripcion"], "respuesta": resp})
    with open(DIR_RESULTADOS / "2_2_respuestas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["archivo", "transcripcion", "respuesta"])
        w.writeheader()
        w.writerows(salida)


if __name__ == "__main__":
    main()
