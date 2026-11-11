# Taller: Entrada multimodal y audio

Desarrollo de Aplicaciones con IA. Dominio: Ragi (asistente RAG sobre TOGAF 9.1).
Visión sobre imágenes y transcripción de audio con la API de Groq.

## Requisitos e instalación

Python 3.10 o superior y una clave de API de Groq.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
```

## Variables de entorno (archivo `.env`)

| Variable | Obligatoria | Por defecto |
|---|---|---|
| `GROQ_API_KEY` | Sí | - |
| `MODELO_VISION` | No | `qwen/qwen3.8-27b` |
| `MODELO_TEXTO` | No | `qwen/qwen3.8-27b` |
| `MODELO_AUDIO` | No | `whisper-large-v3-turbo` |
| `DOMINIO` | No | `el marco de arquitectura empresarial TOGAF 9.1` |

La clave solo va en `.env`, que está en `.gitignore`. No se sube al repositorio.

## Cómo ejecutar cada parte

Ejecuta todo desde la carpeta `taller_multimodal/`. Las salidas se guardan en `resultados/`.

### Parte 1. Visión (imágenes en `imagenes/`)

| Punto | Comando |
|---|---|
| 1.1 Pregunta sobre una imagen | `python parte1_vision/p1_1_pregunta_imagen.py imagen_01.png` |
| 1.2 Extracción estructurada | `python parte1_vision/p1_2_extraccion_estructurada.py` |
| 1.3 Varias imágenes | `python parte1_vision/p1_3_varias_imagenes.py imagen_01.png imagen_02.png imagen_03.png` |
| 1.4 Error provocado | `python parte1_vision/p1_4_error_provocado.py muchas_imagenes` |

- 1.2 compara con los valores reales de `imagenes/valores_reales.json` y usa el esquema de `parte1_vision/schema.py`.
- 1.4 acepta también `mime_incorrecto`, `imagen_grande`, `modelo_sin_vision` o `todos`.

### Parte 2. Audio (audios en `audios/`, datos en `audios/metadatos.csv`)

| Punto | Comando |
|---|---|
| (opcional) Medir duraciones | `python parte2_audio/medir_duraciones.py` |
| 2.1 Transcripción | `python parte2_audio/p2_1_transcripcion.py` |
| 2.2 Respuesta a partir de la transcripción | `python parte2_audio/p2_2_respuesta.py` |

Ejecuta 2.1 antes que 2.2: el segundo usa `resultados/2_1_transcripciones.csv`.

## Estructura

```
taller_multimodal/
├── common.py            utilidades y límites compartidos
├── parte1_vision/       scripts 1.1 a 1.4 y schema.py
├── parte2_audio/        scripts 2.1, 2.2 y medir_duraciones.py
├── imagenes/            imágenes y valores_reales.json
├── audios/              audios y metadatos.csv
├── resultados/          salidas de los scripts
└── informe/             informe y capturas
```
