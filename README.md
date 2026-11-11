# Taller: Entrada multimodal y audio

Asignatura: Desarrollo de Aplicaciones con IA.
Visión (imágenes) y transcripción de audio sobre el dominio del proyecto, con medición de calidad y límites.

## Preparación

```bash
cd taller_multimodal
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # y pega tu GROQ_API_KEY en .env
```

### Variables de entorno

| Variable | Obligatoria | Por defecto |
|---|---|---|
| `GROQ_API_KEY` | Sí | - |
| `MODELO_VISION` | No | `qwen/qwen3.8-27b` |
| `MODELO_TEXTO` | No | `qwen/qwen3.8-27b` |
| `MODELO_AUDIO` | No | `whisper-large-v3-turbo` |
| `DOMINIO` | No | `el marco de arquitectura empresarial TOGAF 9.1` (dominio de Ragi; se usa en el prompt de 2.2) |

> La clave vive solo en `.env`, que está en `.gitignore`. No la escribas en el código ni la subas a ningún commit.

## Antes de ejecutar: qué debes poner

1. **`imagenes/`**: mínimo 5 imágenes de TOGAF 9.1 (figuras del ciclo ADM, Architecture Repository, Enterprise Continuum, Content Framework, tablas o plantillas de entregables como el mapa de stakeholders o la plantilla de principios). Cita la fuente en el informe (jpg/png/webp). Máx. 3 por solicitud y 20 MB por solicitud.
2. **`imagenes/valores_reales.json`**: lo que tú lees en 3 imágenes (nombre del archivo -> campos). Es la referencia para el porcentaje de aciertos.
3. **`parte1_vision/schema.py`**: cambia `CAMPOS` y la clase `Extraccion` por al menos 5 campos útiles de tu dominio.
4. **`audios/`**: mínimo 4 audios de 10 a 30 s (wav, mp3, m4a, ogg o webm; máx. 25 MB), con al menos 2 hablantes y uno con ruido de fondo.
5. **`audios/metadatos.csv`**: archivo, hablante, condición (con/sin ruido), duración y el texto exacto que se dijo.

## Cómo ejecutar cada parte

| Punto | Comando | Salida |
|---|---|---|
| 1.1 Pregunta sobre una imagen | `python parte1_vision/p1_1_pregunta_imagen.py imagen_01.jpg "tu pregunta"` | `resultados/1_1_respuesta.md` |
| 1.2 Extracción estructurada | `python parte1_vision/p1_2_extraccion_estructurada.py` | `resultados/1_2_tabla_aciertos.csv` y % de aciertos en consola |
| 1.3 Varias imágenes | `python parte1_vision/p1_3_varias_imagenes.py imagen_01.jpg imagen_02.jpg` | `resultados/1_3_respuesta.md` |
| 1.4 Error provocado | `python parte1_vision/p1_4_error_provocado.py todos` | `resultados/1_4_errores.md` |
| 2.1 Transcripción | `python parte2_audio/p2_1_transcripcion.py` | `resultados/2_1_transcripciones.csv` (incluye WER) |
| 2.2 Respuesta | `python parte2_audio/p2_2_respuesta.py` | `resultados/2_2_respuestas.csv` |

Orden recomendado: 1.1 -> 1.2 -> 1.3 -> 1.4 -> 2.1 -> 2.2 (2.2 usa la salida de 2.1).

## Validación del JSON (1.2)

El modelo `Extraccion` de `schema.py` (pydantic) rechaza campos faltantes, campos extra y tipos incorrectos. Si la salida no cumple el esquema o no es JSON, el script imprime un aviso y sigue con la siguiente imagen en lugar de fallar.

## Informe

`informe/Informe_Taller_Multimodal.docx` sigue la plantilla de entrega. Llénalo con capturas de la ejecución y la explicación de cada punto. Si te piden PDF, expórtalo desde Word.

## Checklist de entrega

- [ ] Carpeta `taller_multimodal/` en el repositorio del proyecto
- [ ] 5+ imágenes y 4+ audios (o enlace si pesan demasiado)
- [ ] Scripts ejecutables de principio a fin
- [ ] Este README con instrucciones y variables de entorno
- [ ] Ninguna clave de API en el código **ni en el historial de commits**
- [ ] Informe Word/PDF con capturas y análisis de cada punto
