"""2.1 Transcripción de audios desde archivo con Whisper (Groq).
Lee audios/metadatos.csv y guarda resultados/2_1_transcripciones.csv (con WER si hay texto real).
Uso: python parte2_audio/p2_1_transcripcion.py
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import DIR_AUDIOS, DIR_RESULTADOS, MAX_MB_AUDIO, MODELO_AUDIO, cliente


def palabras(t):
    return re.sub(r"[^\w\s]", "", t.lower()).split()


def wer(ref: str, hip: str) -> float:
    """Word Error Rate: distancia de edición entre palabras / palabras de la referencia."""
    r, h = palabras(ref), palabras(hip)
    if not r:
        return float("nan")
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / len(r)


def main():
    meta = DIR_AUDIOS / "metadatos.csv"
    if not meta.exists():
        sys.exit("Falta audios/metadatos.csv (archivo,hablante,condicion,duracion_s,lo_que_se_dijo).")
    client = cliente()
    salida = []
    with open(meta, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta = DIR_AUDIOS / fila["archivo"]
            if not ruta.exists():
                print(f"[AVISO] No existe {ruta.name}, se omite.")
                continue
            mb = ruta.stat().st_size / 1024 / 1024
            if mb > MAX_MB_AUDIO:
                print(f"[AVISO] {ruta.name} pesa {mb:.1f} MB (> {MAX_MB_AUDIO} MB), se omite.")
                continue
            with open(ruta, "rb") as audio:
                r = client.audio.transcriptions.create(
                    file=(ruta.name, audio.read()), model=MODELO_AUDIO,
                    language="es", response_format="text", temperature=0.0)
            texto = (r if isinstance(r, str) else r.text).strip()
            error = wer(fila["lo_que_se_dijo"], texto) if len(fila["lo_que_se_dijo"]) > 5 else float("nan")
            print(f"\n[{ruta.name}] {fila['hablante']} ({fila['condicion']})\n"
                  f"  Dicho: {fila['lo_que_se_dijo']}\n  Transcrito: {texto}\n  WER: {error:.2f}")
            salida.append({**fila, "transcripcion": texto, "wer": round(error, 3)})

    if salida:
        with open(DIR_RESULTADOS / "2_1_transcripciones.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(salida[0].keys()))
            w.writeheader()
            w.writerows(salida)


if __name__ == "__main__":
    main()
