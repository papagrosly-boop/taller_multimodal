"""Utilidades compartidas por todos los scripts del taller."""
import base64
import mimetypes
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

MODELO_VISION = os.getenv("MODELO_VISION", "qwen/qwen3.8-27b")
MODELO_TEXTO = os.getenv("MODELO_TEXTO", "qwen/qwen3.8-27b")
MODELO_AUDIO = os.getenv("MODELO_AUDIO", "whisper-large-v3-turbo")
DOMINIO = os.getenv("DOMINIO", "el marco de arquitectura empresarial TOGAF 9.1")

DIR_IMAGENES = RAIZ / "imagenes"
DIR_AUDIOS = RAIZ / "audios"
DIR_RESULTADOS = RAIZ / "resultados"
DIR_RESULTADOS.mkdir(exist_ok=True)

# Límites documentados por Groq (verifícalos si cambias de modelo o proveedor)
MAX_IMAGENES = 3
MAX_MB_SOLICITUD = 20
MAX_MB_AUDIO = 25
EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp"}


def cliente() -> Groq:
    clave = os.getenv("GROQ_API_KEY")
    if not clave:
        sys.exit("Falta GROQ_API_KEY. Copia .env.example como .env y completa tu clave.")
    return Groq(api_key=clave)


def listar_imagenes() -> list[Path]:
    return sorted(p for p in DIR_IMAGENES.iterdir() if p.suffix.lower() in EXT_IMAGEN)


def data_url(ruta: Path, mime: str | None = None) -> str:
    """Imagen local -> data URL en base64 (mime se deduce de la extensión)."""
    mime = mime or mimetypes.guess_type(ruta.name)[0] or "image/jpeg"
    b64 = base64.b64encode(ruta.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def bloque_imagen(ruta: Path, mime: str | None = None) -> dict:
    return {"type": "image_url", "image_url": {"url": data_url(ruta, mime)}}


def limpiar(texto: str) -> str:
    """Quita bloques <think>...</think> que algunos modelos de razonamiento devuelven."""
    return re.sub(r"<think>.*?</think>", "", texto or "", flags=re.S).strip()


def preguntar_con_imagenes(client: Groq, rutas: list[Path], pregunta: str,
                           modelo: str | None = None, max_tokens: int = 1500) -> str:
    """Envía 1..3 imágenes locales + una pregunta. Valida los límites antes de llamar."""
    if len(rutas) > MAX_IMAGENES:
        raise ValueError(f"Máximo {MAX_IMAGENES} imágenes por solicitud (enviaste {len(rutas)}).")
    mb = sum(p.stat().st_size for p in rutas) * 4 / 3 / 1024 / 1024  # base64 pesa ~33 % más
    if mb > MAX_MB_SOLICITUD:
        raise ValueError(f"La solicitud pesa ~{mb:.1f} MB y el máximo es {MAX_MB_SOLICITUD} MB.")
    contenido = [{"type": "text", "text": pregunta}] + [bloque_imagen(p) for p in rutas]
    r = client.chat.completions.create(
        model=modelo or MODELO_VISION,
        messages=[{"role": "user", "content": contenido}],
        max_tokens=max_tokens,
        temperature=0,
    )
    return limpiar(r.choices[0].message.content)


def guardar(nombre: str, texto: str) -> Path:
    ruta = DIR_RESULTADOS / nombre
    ruta.write_text(texto, encoding="utf-8")
    return ruta
