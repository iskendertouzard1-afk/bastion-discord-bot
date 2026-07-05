import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CSV_PATH = BASE / "data" / "raw" / "burgs.csv"
OUT_BASE = BASE / "data" / "lore" / "paises"

STATE_TO_FOLDER = {
    "Yugure": "yugure",
    "Hihabar": "hihabar",
    "Nosland": "nosland",
    "Varkeldov": "varkeldov",
    "Kobe": "kobe"
}

def tiene(valor):
    return bool(valor and valor.strip())

def ciudad_desde_fila(row):
    return {
        "id_azgaar": int(row["Id"]),
        "nombre": row["Burg"],
        "prefectura": row["Province"],
        "prefectura_nombre_completo": row["Province Full Name"],
        "estado": row["State"],
        "estado_nombre_completo": row["State Full Name"],
        "cultura": row["Culture"],
        "religion": row["Religion"],
        "grupo": row["Group"],
        "poblacion": int(float(row["Population"])),
        "coordenadas": {
            "x": float(row["X"]),
            "y": float(row["Y"]),
            "latitud": float(row["Latitude"]),
            "longitud": float(row["Longitude"])
        },
        "elevacion_m": int(float(row["Elevation (m)"])),
        "temperatura": row["Temperature"],
        "clima_referencia": row["Temperature likeness"],
        "rasgos": {
            "capital": tiene(row["Capital"]),
            "puerto": tiene(row["Port"]),
            "ciudadela": tiene(row["Citadel"]),
            "murallas": tiene(row["Walls"]),
            "plaza": tiene(row["Plaza"]),
            "templo": tiene(row["Temple"]),
            "barrio_pobre": tiene(row["Shanty Town"])
        },
        "descripcion": "",
        "lugares_importantes": [],
        "pnj_relevantes": [],
        "problemas_actuales": [],
        "preview_link": row["Preview link"]
    }

def main():
    ciudades_por_pais = {}

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for row in lector:
            estado = row["State"]
            carpeta = STATE_TO_FOLDER.get(estado)

            if not carpeta:
                continue

            ciudad = ciudad_desde_fila(row)
            ciudades_por_pais.setdefault(carpeta, []).append(ciudad)

    for carpeta, ciudades in ciudades_por_pais.items():
        pais_dir = OUT_BASE / carpeta
        pais_dir.mkdir(parents=True, exist_ok=True)

        salida = pais_dir / "05_ciudades.json"

        data = {
            "titulo": "Ciudades y asentamientos",
            "pais": carpeta,
            "fuente": "Azgaar Fantasy Map Generator",
            "total_ciudades": len(ciudades),
            "ciudades": sorted(ciudades, key=lambda c: c["poblacion"], reverse=True)
        }

        with open(salida, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, indent=2, ensure_ascii=False)

        print(f"Generado: {salida} ({len(ciudades)} ciudades)")

if __name__ == "__main__":
    main()
