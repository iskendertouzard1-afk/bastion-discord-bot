import os
import random
from dotenv import load_dotenv
from openai import OpenAI

import json
from codex_loader import cargar_contexto_codex

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

REINOS = ["Yugure", "Nosland", "Hihabar", "Varkeldov"]

PROMPT_SISTEMA = """
Eres el cronista del Codex de Los Grandes Reinos para una campaña de D&D.
Genera UNA noticia o rumor breve para Discord.

Reglas:
- Escribe en español.
- Extensión: 3 a 6 líneas.
- Debe sonar como noticia, rumor de taberna, informe de caravana o boletín regional.
- Usa tono de fantasía sobria.
- No menciones que eres IA.
- No reveles secretos de DM.
- No inventes eventos enormes como guerras, muertes de gobernantes o cataclismos.
- Puede usar comercio, clima, rutas, religión, nobleza, gremios, viajeros o sucesos extraños menores.
"""

RESUMEN_CODEX = """
Yugure: imperio de estética japonesa/élfica. Honor, equilibrio, Pelor, daimyō, tensiones entre Pacto de Jade y Liga Carmesí.
Nosland: reino feudal-romano. Ley, ciudadanía, Basileus, Senado, Cinco Casas de Ox, Tres Luminarias: Mystra, Tyr y Pelor.
Hihabar: sultanato académico y comercial. Sultán, Diwan Imperial, Moradin, Aleph, Gran Biblioteca, comercio, astronomía y magia.
Varkeldov: reino frío de bosques y castillos. Gran Domnitor, Voivodas, Boyardos, humanos, licántropos, dhampir y vampiros nobles. Selûne, Mystra y Tyr.
"""

def generar_noticia_ia(tipo="aleatorio"):
    contexto = cargar_contexto_codex()

    contexto_texto = json.dumps(
        contexto,
        ensure_ascii=False,
        indent=2
    )

    if tipo == "noticia":
        estilo = "Genera una noticia escrita por un cronista. Debe sonar confiable y oficial."
    elif tipo == "rumor":
        estilo = "Genera un rumor de taberna. Puede sonar incierto, exagerado o contado por viajeros."
    else:
        estilo = "Elige entre noticia de cronista o rumor de taberna."

    respuesta = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {
                "role": "user",
                "content": f"""
Contexto real del Codex:
{contexto_texto}

Tipo solicitado:
{estilo}

Genera una sola entrada para el canal #bastion.
"""
            }
        ],
        temperature=0.9,
        max_output_tokens=220
    )

    return respuesta.output_text.strip()
