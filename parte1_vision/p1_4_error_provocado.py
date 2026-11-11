"""1.4 Errores provocados a propósito. Muestra el mensaje real de la API.
Uso: python parte1_vision/p1_4_error_provocado.py [mime_incorrecto|imagen_grande|muchas_imagenes|modelo_sin_vision|todos]
Elige el caso cuyo error quieras capturar para el informe (el mensaje depende de la API).
"""
import base64
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from groq import APIConnectionError, APIStatusError

from common import MODELO_VISION, bloque_imagen, cliente, guardar, limpiar, listar_imagenes

MODELO_SIN_VISION = "llama-3.1-8b-instant"  # modelo de solo texto


def enviar(client, modelo, contenido):
    r = client.chat.completions.create(model=modelo, max_tokens=200,
                                       messages=[{"role": "user", "content": contenido}])
    return limpiar(r.choices[0].message.content)


def caso(nombre, client, img: Path):
    txt = {"type": "text", "text": "Describe la imagen en una frase."}
    if nombre == "mime_incorrecto":
        b64 = base64.b64encode(img.read_bytes()).decode()
        url = f"data:application/pdf;base64,{b64}"  # tipo declarado que no corresponde
        return enviar(client, MODELO_VISION, [txt, {"type": "image_url", "image_url": {"url": url}}])
    if nombre == "imagen_grande":
        falso = b"\x89PNG\r\n\x1a\n" + os.urandom(25 * 1024 * 1024)  # ~25 MB > límite
        url = "data:image/png;base64," + base64.b64encode(falso).decode()
        return enviar(client, MODELO_VISION, [txt, {"type": "image_url", "image_url": {"url": url}}])
    if nombre == "muchas_imagenes":
        return enviar(client, MODELO_VISION, [txt] + [bloque_imagen(img) for _ in range(4)])
    if nombre == "modelo_sin_vision":
        return enviar(client, MODELO_SIN_VISION, [txt, bloque_imagen(img)])
    raise SystemExit(f"Caso desconocido: {nombre}")


def main():
    imgs = listar_imagenes()
    if not imgs:
        sys.exit("Pon al menos una imagen en imagenes/.")
    elegido = sys.argv[1] if len(sys.argv) > 1 else "muchas_imagenes"
    casos = (["mime_incorrecto", "imagen_grande", "muchas_imagenes", "modelo_sin_vision"]
             if elegido == "todos" else [elegido])
    client, log = cliente(), []
    for c in casos:
        print(f"\n### Caso: {c}")
        try:
            res = caso(c, client, imgs[0])
            msg = f"SIN ERROR (la API aceptó la solicitud). Respuesta: {res[:200]}"
        except APIStatusError as e:
            msg = f"HTTP {e.status_code} -> {e.message}"
        except APIConnectionError as e:
            msg = f"Error de conexión: {e}"
        print(msg)
        log.append(f"## {c}\n{msg}\n")
    guardar("1_4_errores.md", "\n".join(log))


if __name__ == "__main__":
    main()
