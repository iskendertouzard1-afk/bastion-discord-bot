import json
import random
from pathlib import Path

BASE_CODEX = Path("data/lore/paises")

REINOS = {
    "yugure": "Yugure",
    "nosland": "Nosland",
    "hihabar": "Hihabar",
    "varkeldov": "Varkeldov"
}

ARCHIVOS_POR_CATEGORIA = {
    "general": ["00_resumen.json", "02_gobierno.json", "13_relaciones_exteriores.json"],
    "comercio": ["00_resumen.json", "08_economia.json", "13_relaciones_exteriores.json"],
    "politica": ["00_resumen.json", "02_gobierno.json", "06_facciones.json", "10_personajes.json"],
    "religion": ["00_resumen.json", "07_cultura.json", "09_religion.json"],
    "rumor": ["00_resumen.json", "07_cultura.json", "10_personajes.json", "13_relaciones_exteriores.json"]
}


def cargar_json(ruta: Path):
    if not ruta.exists():
        return None

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except Exception as error:
        return {"error": f"No se pudo leer {ruta.name}: {error}"}


def obtener_reino_aleatorio():
    clave = random.choice(list(REINOS.keys()))
    return clave, REINOS[clave]


def obtener_categoria_aleatoria():
    return random.choice(list(ARCHIVOS_POR_CATEGORIA.keys()))


def cargar_contexto_codex(reino_clave=None, categoria=None):
    if reino_clave is None:
        reino_clave, reino_nombre = obtener_reino_aleatorio()
    else:
        reino_nombre = REINOS.get(reino_clave, reino_clave)

    if categoria is None:
        categoria = obtener_categoria_aleatoria()

    carpeta_reino = BASE_CODEX / reino_clave
    archivos = ARCHIVOS_POR_CATEGORIA.get(categoria, ARCHIVOS_POR_CATEGORIA["general"])

    contexto = {
        "reino": reino_nombre,
        "categoria": categoria,
        "archivos_usados": [],
        "contenido": {}
    }

    for nombre_archivo in archivos:
        ruta = carpeta_reino / nombre_archivo
        datos = cargar_json(ruta)

        if datos is not None:
            contexto["archivos_usados"].append(nombre_archivo)
            contexto["contenido"][nombre_archivo] = datos

    return contexto
