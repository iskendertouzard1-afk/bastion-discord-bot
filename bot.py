import os
import json
from openai import OpenAI
import random
from pathlib import Path
from datetime import date
from noticias_rumores_ia import generar_noticia_ia
from datetime import time
from discord.ext import tasks
from noticias_rumores_ia import generar_noticia_ia


import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
print("TOKEN CARGADO:", os.getenv("DISCORD_TOKEN") is not None)

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
ARCHIVO = Path("bastion.json")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

CAUSAS_REFUGIADOS = [
    "un ataque de monstruos",
    "una catástrofe natural",
    "una calamidad desconocida",
    "el saqueo de su aldea",
    "una plaga repentina",
    "un incendio que arrasó sus hogares",
    "la violencia de una facción local",
    "la desaparición de varios líderes comunitarios"
]




OBJETOS_MAGICOS_INFRECUENTES = [
    "Poción de la resistencia acida",
    "Poción trato con animales",
    "Poción de resistencia al frio",
    "Poción aliento de fuego",
    "Poción resistencia al fuego",
    "poción resistencia a la fuerza",
    "Poción de curación mayor",
    "Poción de crecimiento",
    "Poción fuerza gigante de la montaña",
    "Poción resistencia eléctrica",
    "Poción resistencia necrótica",
    "Poción de veneno",
    "Poción resistencia veneno",
    "Póción resistencia físico",
    "Poción de pugilista",
    "Poción resistencia radiante",
    "Poción resistencia trueno",
    "Poción de respirar bajo el agua",
    "Pergamino auxilio",
    "Pergamino alterar", 
    "Pergamino mensajero animal",
    "Pergamino cerradura arcana",
    "Pergamino Vigor acarano",
    "Pergamino Augurio",
    "Pergamino Piel robliza",
    "Pergamino Sentido animal",
    "Pergamino Cegar/ensordecer",
    "Pergamino contorno borroso",
    "Pergamino calmar emociones",
    "Pergamino nube de dagas",
    "Pergamino Corona de la locura",
    "Pergamino oscuridad",
    "Detectar pensamientos",
    "Pergamino aliento de dragón",
    "Pergamino mejorar habilidad",
    "Pergamino agrandar reducir",
    "Pergamino cautivar",
    "Pergamino Encontrar montura",
    "Pergamino Encontrar trampas",
    "Pergamino Hoja de fuego",
    "Pergamino Esfera flamígera",
    "Pergamino Reposo gentil",
    "Pergamino Ráfaga de viento",
    "Pergamino Calentar metal",
    "Pergamino Inmovilizar persona",
    "Pergamino Invisibilidad",
    "Pergamino Abrir cerraduras",
    "Pergamino Restauración menor",
    "Pergamino Levitar",
    "Pergamino Localizar animales o plantas",
    "Pergamino Localizar objeto",
    "Pergamino Boca mágica",
    "Pergamino Arma mágica",
    "Pergamino Flecha ácida de Melf",
    "Pergamino Imagen múltiple",
    "Pergamino Imagen reflejada",
    "Pergamino Paso brumoso",
    "Pergamino Rayo lunar",
    "Pergamino Aura mágica de Nystul",
    "Pergamino Paso sin dejar rastro",
    "Pergamino Fuerza fantasmal",
    "Pergamino Oración de curación",
    "Pergamino Protección contra el veneno",
    "Pergamino Rayo de debilitamiento",
    "Pergamino Cuerda trucada",
    "Pergamino Nube de dagas",
    "Pergamino Ver invisibilidad",
    "Pergamino Romper",
    "Pergamino Golpe fulgurante",
    "Pergamino Silencio",
    "Pergamino Trepar cual arácnido",
    "Pergamino Crecimiento espinoso",
    "Pergamino Arma espiritual",
    "Pergamino Sugestión",
    "Pergamino Ráfaga abrasadora",
    "Pergamino Vínculo protector",
    "Pergamino Telaraña",
    "Pergamino Zona de verdad",
]

def cargar_bastion():
    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}
    datos.setdefault("evento_pendiente", None)
    datos.setdefault("arcas", 0)
    datos.setdefault("suministros", 0)
    datos.setdefault("pociones_curacion", 0)
    datos.setdefault("venenos", 0)
    datos.setdefault("asalariados_detalle", [])
    datos.setdefault("asalariados_detalle", [])
    datos.setdefault("contador_asalariados", 0)
    datos.setdefault("defensores_detalle", [])
    datos.setdefault("contador_defensores", 0)
    datos.setdefault("husped_detalle", None)
    datos.setdefault("contador_huespedes", 0)
    datos.setdefault("refugiados_detalle", None)
    datos.setdefault("contador_refugiados", 0)
    datos.setdefault("acciones_semana", 0)
    datos.setdefault("acciones_diarias", {})
    datos.setdefault("defensores", 0)
    datos.setdefault("refugiados", None)
    datos.setdefault("personajes", {})
    datos.setdefault("asalariados", 0)
    datos.setdefault("instalaciones", {
        "huerto":True,
        "almacen":True,
        "armeria": False,
        "barracon":False,
        "biblioteca": False,
        "estudio arcano": False,
        "herreria": False,
        "santuario": False,
        "taller": False,
        "circulo de transportación": False,
        "establo": False,
        "invernadero": False,
        "laboratorio": False,
        "sacristía": False,
        "sala de juego": False,
        "sala de trofeos": False,
        "scriptorium": False,
        "teatro": False,
        "zona de entrenamiento": False,
        "archivo": False,
        "cámara de meditación": False,
        "casa de fieras": False,
        "observatorio": False,
        "relicario": False,
        "taberna": False,
        "casa gremial": False,
        "sala de operaciones": False,
        "sanctasantórum": False,
        "Semiplano": False
        
    })


    return datos

def calcular_produccion(datos):
    asalariados = datos["asalariados"]
    instalaciones_activas = sum(1 for activa in datos["instalaciones"].values() if activa)

    if asalariados <= 0:
        return 0

    if asalariados < instalaciones_activas:
        return 0.5

    return 1

def guardar_bastion(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def obtener_personaje(datos, usuario_id):
    return datos["personajes"].get(usuario_id)


def puede_actuar(datos, usuario_id):
    hoy = str(date.today())
    return datos["acciones_diarias"].get(usuario_id) != hoy

def tiene_barracon(datos):
    return datos["instalaciones"].get("barracon", False)


def max_defensores(datos):
    if tiene_barracon(datos):
        return 12
    return 6



def costo_defensor(datos):
    if tiene_barracon(datos):
        return 1
    return 2

def registrar_accion(datos, usuario_id):
    datos["acciones_diarias"][usuario_id] = str(date.today())

def procesar_huesped(datos):
    mensaje = ""

    husped = datos.get("husped")
    if not husped:
        return mensaje

    husped["semanas"] -= 1

    if husped["semanas"] > 0:
        datos["husped"] = husped
        return mensaje

    tipo = husped.get("tipo")

    if tipo == "renombre":
        datos.setdefault("inventario", [])
        datos["inventario"].append("Carta de recomendación")

        mensaje = (
            "\n\n🎖️ **El huésped de renombre abandona el bastión.**\n"
            "Antes de partir, entrega una **carta de recomendación**."
        )

    elif tipo == "refugiado":
        recompensa = random.randint(1, 6) * 100
        datos["oro"] += recompensa

        mensaje = (
            "\n\n❤️ **El huésped refugiado abandona el bastión.**\n"
            f"Como agradecimiento, deja un obsequio de **{recompensa} PO**."
        )

    elif tipo == "mercenario":
        if husped.get("ocupa") == "defensor":
            datos["defensores"] = max(0, datos["defensores"] - 1)
            mensaje = (
                "\n\n🛡️ **El mercenario abandona el bastión.**\n"
                "El número de defensores vuelve a la normalidad."
            )
        else:
            datos["asalariados"] = max(0, datos["asalariados"] - 1)
            mensaje = (
                "\n\n🧳 **El mercenario abandona el bastión.**\n"
                "El asalariado temporal deja sus labores."
            )

    elif tipo == "monstruo":
        nombre = husped.get("nombre", "monstruo amistoso")
        mensaje = (
            f"\n\n🐉 **El {nombre} abandona el bastión.**\n"
            "La criatura amistosa vuelve a los caminos salvajes."
        )

    if datos.get("husped_detalle"):
        datos["husped_detalle"]["estado"] = "partió"
        datos["husped_detalle"]["fecha_salida"] = str(date.today())
        datos["husped_detalle"]["motivo_salida"] = "Terminó su estancia en el bastión."

    datos.pop("husped", None)
    return mensaje

def cargar_tabla(nombre):
    ruta = f"data/{nombre}.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def generar_huesped_ia(datos, tipo):
    lore = cargar_tabla("lore")

    prompt = f"""
Crea un huésped para el bastión de una campaña de D&D.

Tipo de huésped:
{tipo}

Lore:
{json.dumps(lore, ensure_ascii=False, indent=2)}

Estado del bastión:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Reglas:
- Responde solo JSON válido.
- No uses markdown.
- Fantasía feudal japonesa.
- El huésped debe encajar con el tipo indicado.
- Historia máxima de 2 frases.
- Si el tipo es monstruo, puede ser criatura amistosa.
- Si el tipo es renombre, debe ser una persona influyente.
- Si el tipo es refugiado, debe ser alguien vulnerable o perseguido.
- Si el tipo es mercenario, debe ser combatiente profesional.

Formato:
{{
  "nombre": "Nombre",
  "tipo": "{tipo}",
  "edad": "Edad o descripción",
  "procedencia": "Lugar",
  "historia": "Historia breve"
}}
"""

    respuesta = openai_client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return json.loads(respuesta.output_text.strip())

def crear_grupo_refugiados(datos, cantidad):
    causa = random.choice(CAUSAS_REFUGIADOS)

    datos["contador_refugiados"] = datos.get("contador_refugiados", 0) + 1

    grupo = {
        "id": datos["contador_refugiados"],
        "categoria": "refugiados",
        "tipo": "grupo",
        "estado": "presente",
        "cantidad": cantidad,
        "causa": causa,
        "procedencia": "Desconocida",
        "historia": f"Un grupo de {cantidad} refugiados llegó al bastión huyendo de {causa}.",
        "fecha_llegada": str(date.today())
    }

    datos["refugiados_detalle"] = grupo
    datos["refugiados"] = {
        "cantidad": cantidad,
        "id": grupo["id"]
    }

    return grupo

def crear_huesped(datos, tipo, semanas, extra=None):
    try:
        huesped = generar_huesped_ia(datos, tipo)
    except Exception:
        huesped = {
            "nombre": "Huésped sin nombre",
            "tipo": tipo,
            "edad": "Desconocida",
            "procedencia": "Desconocida",
            "historia": "Llegó al bastión buscando refugio temporal."
        }

    datos["contador_huespedes"] = datos.get("contador_huespedes", 0) + 1

    huesped["id"] = datos["contador_huespedes"]
    huesped["categoria"] = "huesped"
    huesped["estado"] = "presente"
    huesped["semanas"] = semanas
    huesped["fecha_llegada"] = str(date.today())

    if extra:
        huesped.update(extra)

    datos["husped_detalle"] = huesped

    return huesped

def generar_rumor_ia(datos):
    lore = cargar_tabla("lore")

    prompt = f"""
Eres un cronista de caminos para una campaña de D&D.

Genera un rumor, noticia o mensaje breve que llegue exclusivamente al bastión.

Lore del mundo:
{json.dumps(lore, ensure_ascii=False, indent=2)}

Estado actual del bastión:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Reglas:
- Escribe en español.
- Máximo 4 frases.
- Tono evocador, de fantasía feudal japonesa.
- No reveles secretos importantes.
- No resuelvas tramas principales.
- El texto debe sentirse útil para ambientar la campaña.
- No uses listas.
"""

    respuesta = openai_client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return respuesta.output_text.strip()

def generar_defensor_ia(datos):
    lore = cargar_tabla("lore")

    prompt = f"""
Crea un defensor para el bastión de una campaña de D&D.

Lore:
{json.dumps(lore, ensure_ascii=False, indent=2)}

Estado del bastión:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Reglas:
- Responde solo JSON válido.
- No uses markdown.
- Fantasía feudal japonesa.
- Persona común entrenada para defender el bastión.
- No debe ser un héroe poderoso.
- Historia máxima de 2 frases.

Formato:
{{
  "nombre": "Nombre",
  "rol": "Guardia, arquero, lancero, explorador o veterano",
  "edad": 30,
  "procedencia": "Lugar",
  "historia": "Historia breve"
}}
"""

    respuesta = openai_client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return json.loads(respuesta.output_text.strip())


def crear_defensor(datos, origen="regularizado"):
    try:
        defensor = generar_defensor_ia(datos)
    except Exception:
        defensor = {
            "nombre": "Defensor sin nombre",
            "rol": "Guardia del bastión",
            "edad": 30,
            "procedencia": "Desconocida",
            "historia": "Se unió a la defensa del bastión buscando paga, techo y propósito."
        }

    datos["contador_defensores"] = datos.get("contador_defensores", 0) + 1

    defensor["id"] = datos["contador_defensores"]
    defensor["tipo"] = "defensor"
    defensor["estado"] = "activo"
    defensor["origen"] = origen
    defensor["fecha_registro"] = str(date.today())

    return defensor


def perder_defensores(datos, cantidad, motivo):
    caidos = []

    cantidad = min(cantidad, datos.get("defensores", 0))
    datos["defensores"] = max(0, datos.get("defensores", 0) - cantidad)

    for defensor in datos.get("defensores_detalle", []):
        if len(caidos) >= cantidad:
            break

        if defensor.get("estado") == "activo":
            defensor["estado"] = "fallecido"
            defensor["motivo_salida"] = motivo
            defensor["fecha_salida"] = str(date.today())
            caidos.append(defensor)

    return caidos

def retirar_defensores(datos, cantidad, motivo, estado="abandono"):
    retirados = []

    cantidad = min(cantidad, datos.get("defensores", 0))
    datos["defensores"] = max(0, datos.get("defensores", 0) - cantidad)

    for defensor in datos.get("defensores_detalle", []):
        if len(retirados) >= cantidad:
            break

        if defensor.get("estado") == "activo":
            defensor["estado"] = estado
            defensor["motivo_salida"] = motivo
            defensor["fecha_salida"] = str(date.today())
            retirados.append(defensor)

    return retirados

def generar_asalariado_ia(datos):
    lore = cargar_tabla("lore")

    prompt = f"""
Eres un cronista de una campaña de D&D.

Crea un asalariado nuevo para el bastión.

Lore:
{json.dumps(lore, ensure_ascii=False, indent=2)}

Estado del bastión:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Reglas:
- Responde solo en JSON válido.
- No uses markdown.
- El personaje debe encajar con fantasía feudal japonesa.
- No debe ser héroe poderoso.
- Debe ser alguien útil para labores comunes del bastión.
- El nombre debe sonar adecuado al mundo de Tatay.
- La historia debe tener máximo 2 frases.

Formato exacto:
{
  "nombre": "Nombre del asalariado",
  "oficio": "Oficio breve",
  "historia": "Historia breve"
}
"""

    respuesta = openai_client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    texto = respuesta.output_text.strip()
    return json.loads(texto)

def generar_asalariado_ia(datos):
    lore = cargar_tabla("lore")

    prompt = f"""
Crea un asalariado para el bastión de una campaña de D&D.

Lore:
{json.dumps(lore, ensure_ascii=False, indent=2)}

Estado del bastión:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Reglas:
- Responde solo JSON válido.
- No uses markdown.
- Fantasía feudal japonesa.
- Persona común, no héroe poderoso.
- Historia máxima de 2 frases.

Formato:
{{
  "nombre": "Nombre",
  "oficio": "Oficio breve",
  "edad": 30,
  "procedencia": "Lugar",
  "historia": "Historia breve"
}}
"""

    respuesta = openai_client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return json.loads(respuesta.output_text.strip())

def perder_asalariados(datos, cantidad, motivo):
    perdidos = []

    cantidad = min(cantidad, datos.get("asalariados", 0))
    datos["asalariados"] = max(0, datos.get("asalariados", 0) - cantidad)

    for asalariado in datos.get("asalariados_detalle", []):
        if len(perdidos) >= cantidad:
            break

        if asalariado.get("estado") == "activo":
            asalariado["estado"] = "abandono"
            asalariado["motivo_salida"] = motivo
            asalariado["fecha_salida"] = str(date.today())
            perdidos.append(asalariado)

    return perdidos

def crear_asalariado(datos):
    try:
        asalariado = generar_asalariado_ia(datos)
    except Exception:
        asalariado = {
            "nombre": "Asalariado sin nombre",
            "oficio": "Trabajador común",
            "edad": 30,
            "procedencia": "Desconocida",
            "historia": "Llegó al bastión buscando empleo estable y techo seguro."
        }

    datos["contador_asalariados"] = datos.get("contador_asalariados", 0) + 1

    asalariado["id"] = datos["contador_asalariados"]
    asalariado["estado"] = "activo"
    asalariado["contratado_semana"] = datos.get("acciones_semana", 0)

    return asalariado

def tirar_tesoro():
    tesoros = cargar_tabla("tesoros")
    tirada = random.randint(1, 100)

    categoria = None
    for entrada in tesoros["tabla_principal"]:
        if entrada["min"] <= tirada <= entrada["max"]:
            categoria = entrada["categoria"]
            break

    tesoro = random.choice(tesoros[categoria])

    return tirada, categoria, tesoro

def procesar_refugiados(datos):
    refugiados = datos.get("refugiados")

    if not refugiados:
        return ""

    cantidad = refugiados.get("cantidad", 0)

    if cantidad <= 0:
        if datos.get("refugiados_detalle"):
            datos["refugiados_detalle"]["estado"] = "partieron"
            datos["refugiados_detalle"]["fecha_salida"] = str(date.today())
            datos["refugiados_detalle"]["motivo_salida"] = "Abandonaron el bastión tras un ataque."
        return ""

    ganancia = random.randint(1, 4) * 10
    datos["arcas"] += ganancia

    return (
        "\n\n🏕️ **Los refugiados colaboran en el bastión.**\n"
        f"Actualmente viven aquí **{cantidad}** refugiados.\n"
        f"Esta semana ayudan en distintas labores y generan **{ganancia} PO**."
    )


HORA_NOTICIAS = time(hour=7, minute=0)

@tasks.loop(time=HORA_NOTICIAS)
async def noticia_diaria():
    canal = discord.utils.get(bot.get_all_channels(), name="bastion")

    if canal is None:
        return

    texto = generar_noticia_ia(tipo="noticia")

    await canal.send(
        f"📰 **Diario de los Grandes Reinos**\n\n{texto}"
    )

def generar_evento_semanal(datos):

    tirada = random.randint(1, 100)
    tirada = 83

    if tirada <= 50:
        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "🌤️ Todo va bien.\n\n"
            "La semana transcurre sin incidentes. "
            "Los asalariados cumplen sus labores, los defensores mantienen la vigilancia "
            "y el bastión conserva su rutina habitual."
        )
    
    if 51 <= tirada <= 53:
        datos["evento_pendiente"] = {
        "tipo": "asalariado_criminal"
    }

        return (
        "🎲 **Evento semanal**\n\n"
        f"Tirada: **{tirada}**\n"
        "⚠️ **Asalariado criminal**\n\n"
        "Uno de los asalariados del bastión ha sido reconocido por agentes del poder local. "
        "Tiene una orden de captura pendiente.\n\n"
        "**Opciones:**\n"
        "`!resolver entregar` — Entregarlo a las autoridades. Pierdes **1 asalariado**.\n"
        "`!resolver sobornar` — Pagar un soborno de **1d6 × 100 PO**."
    )

    if 54 <= tirada <= 56:
        perdidos = random.randint(1, 4)
        perdidos = min(perdidos, datos["asalariados"])

        abandonaron = perder_asalariados(
            datos,
            perdidos,
            "Abandonó el bastión buscando mejores oportunidades."
        )

        mensaje_abandono = ""

        if abandonaron:
            nombres = ", ".join(a.get("nombre", "Asalariado sin nombre") for a in abandonaron)
            mensaje_abandono = (
                f"\n\n🚶 Abandonan el bastión:\n"
                f"**{nombres}**"
            )

        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "🚶 **Asalariados perdidos**\n\n"
            f"**{perdidos}** asalariado(s) abandonan el bastión en busca de mejores oportunidades.\n\n"
            f"👷 Asalariados restantes: **{datos['asalariados']}**"
            f"{mensaje_abandono}"
        )

    if 57 <= tirada <= 61:
        husped = datos.get("husped")
        if husped and husped.get("tipo") == "monstruo" and husped.get("protege"):
            nombre = husped.get("nombre", "monstruo amistoso")

            mensaje_refugiados = ""
            if datos.get("refugiados"):
                cantidad_refugiados = datos["refugiados"].get("cantidad", 0)
            if datos.get("refugiados_detalle"):
                datos["refugiados_detalle"]["estado"] = "partieron"
                datos["refugiados_detalle"]["fecha_salida"] = str(date.today())
                datos["refugiados_detalle"]["motivo_salida"] = "Abandonaron el bastión tras un ataque."

                mensaje_refugiados = (
                    f"\n\n🏃 **Los refugiados abandonan el bastión.**\n"
                    f"Aunque el ataque fue repelido, los **{cantidad_refugiados}** refugiados deciden marcharse."
                )

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "⚔️ **Ataque al bastión**\n\n"
                f"🐉 El **{nombre}** sale a defender el bastión.\n"
                "Los atacantes son repelidos antes de causar bajas.\n\n"
                "🛡️ Defensores perdidos: **0**\n"
                f"🛡️ Defensores restantes: **{datos['defensores']}**"
                f"{mensaje_refugiados}"
            )
        dados = [random.randint(1, 6) for _ in range(6)]
        bajas = dados.count(1)

        defensores_antes = datos["defensores"]
        bajas_reales = min(bajas, defensores_antes)

        caidos = perder_defensores(
            datos,
            bajas_reales,
            "Murió defendiendo el bastión."
        )

        mensaje_caidos = ""
        if caidos:
            nombres = ", ".join(d["nombre"] for d in caidos)
            mensaje_caidos = (
                f"\n\n☠️ Defensores caídos:\n"
                f"**{nombres}**"
            )

        mensaje_instalacion = ""

        if datos["defensores"] == 0:
            instalaciones_activas = [
                nombre for nombre, activa in datos["instalaciones"].items()
                if activa
            ]

            if instalaciones_activas:
                instalacion_dañada = random.choice(instalaciones_activas)
                datos["instalaciones"][instalacion_dañada] = False

                mensaje_instalacion = (
                    f"\n\n🏚️ Como el bastión quedó sin defensores, "
                    f"la instalación **{instalacion_dañada}** queda deshabilitada."
                )

        mensaje_refugiados = ""
        if datos.get("refugiados"):
            cantidad_refugiados = datos["refugiados"].get("cantidad", 0)
        if datos.get("refugiados_detalle"):
            datos["refugiados_detalle"]["estado"] = "partieron"
            datos["refugiados_detalle"]["fecha_salida"] = str(date.today())
            datos["refugiados_detalle"]["motivo_salida"] = "Abandonaron el bastión tras un ataque."

            mensaje_refugiados = (
                f"\n\n🏃 **Los refugiados abandonan el bastión.**\n"
                f"Tras el ataque, los **{cantidad_refugiados}** refugiados deciden continuar su camino."
            )

        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "⚔️ **Ataque al bastión**\n\n"
            f"Dados de ataque: **{dados}**\n"
            f"Resultados de 1: **{bajas}**\n"
            f"🛡️ Defensores perdidos: **{bajas_reales}**\n"
            f"🛡️ Defensores restantes: **{datos['defensores']}**"
            f"{mensaje_instalacion}"
            f"{mensaje_refugiados}"
            f"{mensaje_caidos}"
        )



    if 62 <= tirada <= 65:
        objeto = random.choice(OBJETOS_MAGICOS_INFRECUENTES)

        return (
        "🎲 **Evento semanal**\n\n"
        f"Tirada: **{tirada}**\n"
        "✨ **Descubrimiento mágico**\n\n"
        "Durante sus labores, los asalariados encuentran o comercian un objeto mágico menor.\n\n"
        f"🎁 Objeto obtenido: **{objeto}**"
    )

    if 66 <= tirada <= 69:
        resultado = random.randint(1, 4)

        if resultado == 1:
            huesped = crear_huesped(
                datos,
                tipo="renombre",
                semanas=27
            )

            datos["husped"] = {
                "tipo": "renombre",
                "nombre": huesped.get("nombre"),
                "semanas": 27,
                "id": huesped.get("id")
            }

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🏛️ **Huésped de renombre**\n\n"
                f"**{huesped.get('nombre')}** llega al bastión y solicita alojamiento.\n"
                f"Procedencia: **{huesped.get('procedencia', 'Desconocida')}**\n\n"
                f"_{huesped.get('historia', 'Sin historia registrada.')}_\n\n"
                "Permanecerá durante **27 turnos de bastión**.\n"
                "Cuando abandone el bastión, entregará una **carta de recomendación**."
            )

        if resultado == 2:
            huesped = crear_huesped(
                datos,
                tipo="refugiado",
                semanas=1
            )

            datos["husped"] = {
                "tipo": "refugiado",
                "nombre": huesped.get("nombre"),
                "semanas": 1,
                "id": huesped.get("id")
            }

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🕯️ **Huésped refugiado**\n\n"
                f"**{huesped.get('nombre')}** pide asilo en el bastión.\n"
                f"Procedencia: **{huesped.get('procedencia', 'Desconocida')}**\n\n"
                f"_{huesped.get('historia', 'Sin historia registrada.')}_\n\n"
                "Permanecerá durante **1 turno de bastión**.\n"
                "Cuando parta, dejará un obsequio de **1d6 × 100 PO**."
            )

        if resultado == 3:
            if datos["defensores"] < max_defensores(datos):
                datos["defensores"] += 1
                ocupa = "defensor"
                efecto = "Mientras permanezca en el bastión, proporciona **+1 defensor**."
            else:
                datos["asalariados"] += 1
                ocupa = "asalariado"
                efecto = (
                    "El bastión ya tiene el máximo de defensores, así que el mercenario "
                    "ayudará como **asalariado temporal**."
                )

            huesped = crear_huesped(
                datos,
                tipo="mercenario",
                semanas=4,
                extra={"ocupa": ocupa}
            )

            datos["husped"] = {
                "tipo": "mercenario",
                "nombre": huesped.get("nombre"),
                "semanas": 4,
                "ocupa": ocupa,
                "id": huesped.get("id")
            }

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🛡️ **Huésped mercenario**\n\n"
                f"**{huesped.get('nombre')}** ofrece sus servicios al bastión.\n"
                f"Procedencia: **{huesped.get('procedencia', 'Desconocida')}**\n\n"
                f"_{huesped.get('historia', 'Sin historia registrada.')}_\n\n"
                "Permanecerá durante **4 turnos de bastión**.\n"
                f"{efecto}"
            )

        if resultado == 4:
            monstruo = random.choice(cargar_tabla("monstruos_amistosos"))

            huesped = crear_huesped(
                datos,
                tipo="monstruo",
                semanas=4,
                extra={
                    "especie": monstruo,
                    "protege": True
                }
            )

            datos["husped"] = {
                "tipo": "monstruo",
                "nombre": huesped.get("nombre"),
                "especie": monstruo,
                "semanas": 4,
                "protege": True,
                "id": huesped.get("id")
            }

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🐉 **Huésped monstruoso amistoso**\n\n"
                f"Un **{monstruo}** llamado **{huesped.get('nombre')}** llega al bastión con actitud pacífica.\n"
                f"Procedencia: **{huesped.get('procedencia', 'Desconocida')}**\n\n"
                f"_{huesped.get('historia', 'Sin historia registrada.')}_\n\n"
                "Permanecerá durante **4 turnos de bastión**.\n"
                "Mientras sea huésped, defenderá el bastión durante cualquier ataque."
            )

    if 70 <= tirada <= 74:
        costo = 50

        if datos["arcas"] < costo:
            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🌟 **Oportunidad extraordinaria**\n\n"
                "Se presenta una oportunidad importante para el bastión, "
                "pero las arcas no tienen los **50 PO** necesarios para financiarla.\n\n"
                "La oportunidad se pierde sin consecuencias."
            )

        datos["arcas"] -= costo
        resultado = random.randint(1, 4)
        prueba = random.randint(1, 20)

        if resultado == 1:
            if prueba > 10:
                datos["arcas"] += 1000
                return (
                    "🎲 **Evento semanal**\n\n"
                    f"Tirada: **{tirada}**\n"
                    "🎪 **Festival en el bastión**\n\n"
                    "El bastión financia una celebración local por **50 PO**.\n"
                    f"Tirada de oportunidad: **{prueba}**\n\n"
                    "El festival atrae comerciantes, viajeros y curiosos.\n"
                    "Ganancia obtenida: **1000 PO**."
                )

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🎪 **Festival en el bastión**\n\n"
                "El bastión financia una celebración local por **50 PO**.\n"
                f"Tirada de oportunidad: **{prueba}**\n\n"
                "La celebración anima la región, pero no genera ganancias."
            )

        if resultado == 2:
            if prueba > 10:
                hechizo = random.choice(cargar_tabla("hechizos_nivel_6"))
                datos.setdefault("inventario", [])
                datos["inventario"].append(f"Papiro con el hechizo {hechizo}")

                return (
                    "🎲 **Evento semanal**\n\n"
                    f"Tirada: **{tirada}**\n"
                    "📜 **Investigador arcano**\n\n"
                    "El bastión financia el trabajo de un investigador por **50 PO**.\n"
                    f"Tirada de oportunidad: **{prueba}**\n\n"
                    "El investigador deja preparado un papiro mágico.\n"
                    f"Objeto obtenido: **Papiro con el hechizo {hechizo}**."
                )

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "📜 **Investigador arcano**\n\n"
                "El bastión financia el trabajo de un investigador por **50 PO**.\n"
                f"Tirada de oportunidad: **{prueba}**\n\n"
                "La investigación no produce resultados útiles esta semana."
            )

        if resultado == 3:
            if prueba > 10:
                recompensa = random.randint(1, 10) * 100
                datos["arcas"] += recompensa
                datos.setdefault("inventario", [])
                datos["inventario"].append("Carta de recomendación")

                return (
                    "🎲 **Evento semanal**\n\n"
                    f"Tirada: **{tirada}**\n"
                    "👑 **Noble complacido**\n\n"
                    "El bastión invierte **50 PO** para atender a un noble influyente.\n"
                    f"Tirada de oportunidad: **{prueba}**\n\n"
                    f"El noble queda satisfecho y entrega **{recompensa} PO**.\n"
                    "También deja una **carta de recomendación**."
                )

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "👑 **Noble complacido**\n\n"
                "El bastión invierte **50 PO** para atender a un noble influyente.\n"
                f"Tirada de oportunidad: **{prueba}**\n\n"
                "El noble acepta la hospitalidad, pero no ofrece recompensa."
            )

        if resultado == 4:
            if prueba >= 10:
                ganancia = random.randint(1, 10) * 100
                datos["arcas"] += ganancia

                return (
                    "🎲 **Evento semanal**\n\n"
                    f"Tirada: **{tirada}**\n"
                    "💎 **Artículo de alto valor**\n\n"
                    "Llega al bastión un objeto valioso. "
                    "Los asalariados invierten **50 PO** para negociar su adquisición.\n"
                    f"Tirada de oportunidad: **{prueba}**\n\n"
                    f"La negociación tiene éxito y el objeto se revende con ganancia.\n"
                    f"Ganancia obtenida: **{ganancia} PO**."
                )

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "💎 **Artículo de alto valor**\n\n"
                "Llega al bastión un objeto valioso. "
                "Los asalariados invierten **50 PO** para negociar su adquisición.\n"
                f"Tirada de oportunidad: **{prueba}**\n\n"
                "La negociación fracasa y no se obtiene ganancia."
            )

    if 90 <= tirada <= 100:
        tirada_tesoro, categoria, tesoro = tirar_tesoro()

        nombre = tesoro.get("nombre", "Tesoro desconocido")
        valor = tesoro.get("valor")
        rareza = tesoro.get("rareza")

        datos.setdefault("inventario", [])
        datos["inventario"].append(nombre)

        detalle = ""
        if valor:
            detalle = f"Valor estimado: **{valor} PO**."
        elif rareza:
            detalle = f"Rareza: **{rareza}**."

        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "💰 **Tesoro descubierto**\n\n"
            "Los habitantes del bastión descubren un tesoro inesperado.\n\n"
            f"Tirada de tesoro: **{tirada_tesoro}**\n"
            f"Objeto obtenido: **{nombre}**\n"
            f"{detalle}\n\n"
            "El objeto ha sido agregado al inventario del bastión."
        )

    if 82 <= tirada <= 89:
        cantidad = random.randint(2, 4) + random.randint(1, 4)
        grupo = crear_grupo_refugiados(datos, cantidad)

        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "🏕️ **Refugiados**\n\n"
            f"Un grupo de **{cantidad}** refugiados llega al bastión huyendo de **{grupo['causa']}**.\n"
            "Buscan protección, alimento y un lugar seguro para recuperarse.\n\n"
            "Mientras permanezcan en el bastión, colaborarán con pequeñas labores "
            "y generarán **1d4 × 10 PO** cada semana.\n\n"
            "Si el bastión es atacado, los refugiados abandonarán el lugar."
        )

    if 75 <= tirada <= 81:
        defensores_totales = datos.get("defensores", 0)
        mision = random.choice(cargar_tabla("misiones_ayuda"))

        if defensores_totales <= 0:
            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🛡️ **Petición de ayuda**\n\n"
                f"Un líder local solicita ayuda para **{mision}**.\n\n"
                "El bastión no dispone de defensores para responder a la petición."
            )

        defensores_enviados = max(1, defensores_totales // 2)
        dados = [random.randint(1, 6) for _ in range(defensores_enviados)]
        total = sum(dados)
        texto_dados = " + ".join(str(dado) for dado in dados)

        if total >= 10:
            recompensa = random.randint(1, 6) * 100
            datos["arcas"] += recompensa

            return (
                "🎲 **Evento semanal**\n\n"
                f"Tirada: **{tirada}**\n"
                "🛡️ **Petición de ayuda**\n\n"
                f"Un líder local solicita ayuda para **{mision}**.\n\n"
                f"Se envían **{defensores_enviados}** defensores del bastión.\n"
                f"Dados: **{texto_dados} = {total}**\n\n"
                "La misión se resuelve con éxito.\n\n"
                f"💰 Recompensa obtenida: **{recompensa} PO**.\n"
                f"🏯 Arcas actuales: **{datos['arcas']} PO**."
            )

        recompensa = (random.randint(1, 6) * 100) // 2

        datos["arcas"] += recompensa

        caidos = perder_defensores(
            datos,
            1,
            "Murió durante una misión de ayuda."
        )

        mensaje_caidos = ""

        if caidos:
            mensaje_caidos = (
                f"\n\n☠️ Ha caído **{caidos[0]['nombre']}**."
            )

        return (
            "🎲 **Evento semanal**\n\n"
            f"Tirada: **{tirada}**\n"
            "🛡️ **Petición de ayuda**\n\n"
            f"Un líder local solicita ayuda para **{mision}**.\n\n"
            f"Se envían **{defensores_enviados}** defensores del bastión.\n"
            f"Dados: **{texto_dados} = {total}**\n\n"
            "La misión se completa, aunque el resultado es costoso.\n"
            "Uno de los defensores pierde la vida durante la expedición.\n\n"
            f"💰 Recompensa reducida: **{recompensa} PO**.\n"
            f"🛡️ Defensores restantes: **{datos['defensores']}**.\n"
            f"🏯 Arcas actuales: **{datos['arcas']} PO**."
            f"{mensaje_caidos}"
        )

    return (
    "🎲 **Evento semanal**\n\n"
    f"Tirada: **{tirada}**\n"
    "⚙️ Este evento todavía no está programado."
    )

def avanzar_semana(datos):
    
    

    if datos["acciones_semana"] < 28:
        return None

    datos["acciones_semana"] = 0

    mensaje_evento = generar_evento_semanal(datos)
    mensaje_huesped = procesar_huesped(datos)
    mensaje_refugiados = procesar_refugiados(datos)

    asalariados = datos["asalariados"]
    defensores = datos.get("defensores", 0)
    tiene_barracon = datos["instalaciones"].get("barracon", False)

    costo_asalariados = asalariados
    costo_por_defensor = 1 if tiene_barracon else 2
    costo_defensores = defensores * costo_por_defensor
    costo_total = costo_asalariados + costo_defensores

    mensaje_barracon = ""
    if defensores > 0 and not tiene_barracon:
        mensaje_barracon = (
            "\n\n🏕️ El bastión no tiene barracón. "
            "Los defensores han acampado dentro del bastión, "
            "por lo que cada uno cobra **2 PO** esta semana."
        )

    mensaje_final = f"\n\n{mensaje_evento}{mensaje_huesped}{mensaje_refugiados}"

    if costo_total <= 0:
        return (
            "📜 **Fin de semana del bastión**\n\n"
            "No hay personal que cobre salario."
            f"{mensaje_final}"
        )

    if datos["arcas"] >= costo_total:
        datos["arcas"] -= costo_total

        return (
            "📜 **Fin de semana del bastión**\n\n"
            f"👷 Asalariados: **{asalariados}** → **{costo_asalariados} PO**\n"
            f"🛡️ Defensores: **{defensores}** → **{costo_defensores} PO**\n"
            f"💰 Salarios pagados: **{costo_total} PO**\n"
            f"🏯 Arcas restantes: **{datos['arcas']} PO**"
            f"{mensaje_barracon}"
            f"{mensaje_final}"
        )

    oro_disponible = datos["arcas"]

    asalariados_pagados = min(asalariados, oro_disponible)
    oro_disponible -= asalariados_pagados

    defensores_pagados = min(defensores, oro_disponible // costo_por_defensor)
    oro_disponible -= defensores_pagados * costo_por_defensor

    asalariados_que_se_van = asalariados - asalariados_pagados
    defensores_que_se_van = defensores - defensores_pagados

    datos["arcas"] = oro_disponible

    asalariados_retirados = perder_asalariados(
        datos,
        asalariados_que_se_van,
        "Abandonó el bastión por falta de pago."
    )

    defensores_retirados = retirar_defensores(
        datos,
        defensores_que_se_van,
        "Abandonó la defensa del bastión por falta de pago.",
        estado="abandono"
    )

    if datos["asalariados"] == 0 and datos["defensores"] == 0:
        return (
            "📜 **Fin de semana en la Casa de las Máscaras**\n\n"
            "💰 Las arcas están vacías.\n\n"
            "👷 Los asalariados abandonan el bastión en busca de un empleador que pueda pagar su trabajo.\n"
            "🛡️ Los defensores levantan el campamento y parten hacia otras tierras.\n\n"
            "🏚️ El bastión queda prácticamente deshabitado.\n"
            "🏯 Arcas restantes: **0 PO**"
            f"{mensaje_barracon}"
            f"{mensaje_final}"
        )

    return (
        "📜 **Fin de semana en la Casa de las Máscaras**\n\n"
        "💰 Las arcas no alcanzaron para pagar a todo el personal.\n\n"
        f"👷 Asalariados pagados: **{asalariados_pagados}/{asalariados}**\n"
        f"🛡️ Defensores pagados: **{defensores_pagados}/{defensores}**\n\n"
        f"🚶 Se marchan **{asalariados_que_se_van}** asalariados "
        f"y **{defensores_que_se_van}** defensores.\n\n"
        f"🏚️ El bastión queda con **{datos['asalariados']}** asalariados "
        f"y **{datos['defensores']}** defensores.\n"
        f"🏯 Arcas restantes: **{datos['arcas']} PO**"
        f"{mensaje_barracon}"
        f"{mensaje_final}"
    )


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    if not noticia_diaria.is_running():
        noticia_diaria.start()


@bot.command()
async def ayuda(ctx):
    await ctx.send(
        "🏯 **Casa de las Máscaras - Centro de Ayuda**\n\n"

        "═══════════════════════\n"
        "📊 **Información del Bastión**\n"
        "═══════════════════════\n"
        "`!estado` → Estado general del bastión.\n"
        "`!inventario` → Inventario completo.\n"
        "`!registro` → Registro de habitantes.\n"
        "`!ficha <id o nombre>` → Información detallada de un habitante.\n\n"

        "═══════════════════════\n"
        "👷 **Asalariados**\n"
        "═══════════════════════\n"
        "`!contratar` → Contrata un asalariado (100 PO).\n"
        "`!despedirasalariado <id o nombre>` → Despide un asalariado.\n"
        "`!asalariados` → Lista los asalariados activos.\n"
        #"`!actualizarasalariados` → Genera fichas para asalariados antiguos.\n\n"

        "═══════════════════════\n"
        "🛡️ **Defensores**\n"
        "═══════════════════════\n"
        #"`!contratardefensor` → Contrata un defensor (100 PO).\n"
        #"`!despedirdefensor <id o nombre>` → Despide un defensor.\n"
        "`!defensores` → Lista los defensores activos.\n"
        #"`!actualizardefensores` → Genera fichas para defensores antiguos.\n\n"

        "═══════════════════════\n"
        "🎭 **Huéspedes**\n"
        "═══════════════════════\n"
        #"`!retirarhuesped` → Finaliza manualmente la estancia del huésped actual.\n\n"

        "═══════════════════════\n"
        "💰 **Economía**\n"
        "═══════════════════════\n"
        "`!almacen` → Un asalariado trabaja en el almacén.\n"
        "`!huerto` → Un asalariado trabaja en el huerto.\n\n"

        "═══════════════════════\n"
        "👤 **Administración**\n"
        "═══════════════════════\n"
        "`!registrar` → Vincula tu usuario con un personaje.\n"
        "`!ayuda` → Muestra este panel.\n"
    )


@bot.command()
async def estado(ctx):
    datos = cargar_bastion()

    huesped = datos.get("husped")
    refugiados = datos.get("refugiados")
    instalaciones = datos.get("instalaciones", {})
    inventario = datos.get("inventario", [])

    instalaciones_activas = [
        nombre for nombre, activa in instalaciones.items()
        if activa
    ]

    instalaciones_inactivas = [
        nombre for nombre, activa in instalaciones.items()
        if not activa
    ]

    if huesped:
        texto_huesped = (
            f"🎭 **Huésped:** {huesped.get('nombre', 'Sin nombre')}\n"
            f"Tipo: **{huesped.get('tipo', 'Desconocido')}**\n"
            f"Turnos restantes: **{huesped.get('semanas', '?')}**"
        )
    else:
        texto_huesped = "🎭 **Huésped:** Ninguno"

    if refugiados:
        texto_refugiados = (
            f"🏕️ **Refugiados:** {refugiados.get('cantidad', 0)} personas"
        )
    else:
        texto_refugiados = "🏕️ **Refugiados:** Ninguno"

    texto_instalaciones = "Ninguna"
    if instalaciones_activas:
        texto_instalaciones = ", ".join(instalaciones_activas)

    texto_danadas = "Ninguna"
    if instalaciones_inactivas:
        texto_danadas = ", ".join(instalaciones_inactivas)

    texto_inventario = "Vacío"
    if inventario:
        texto_inventario = f"{len(inventario)} objeto(s). Usa `!inventario` para ver detalle."

    mensaje = (
        "🏯 **Estado de la Casa de las Máscaras**\n\n"

        "💰 **Recursos**\n"
        f"Arcas: **{datos['arcas']} PO**\n"
        f"Suministros: **{datos['suministros']}**\n"
        f"Pociones de curación: **{datos['pociones_curacion']}**\n"
        f"Viales de veneno: **{datos['venenos']}**\n\n"

        "👥 **Habitantes**\n"
        f"Asalariados: **{datos['asalariados']}**\n"
        f"Defensores: **{datos['defensores']}/{max_defensores(datos)}**\n"
        f"{texto_refugiados}\n"
        f"{texto_huesped}\n\n"

        "🏠 **Instalaciones activas**\n"
        f"{texto_instalaciones}\n\n"

        "🏚️ **Instalaciones inactivas**\n"
        f"{texto_danadas}\n\n"

        "🎒 **Inventario**\n"
        f"{texto_inventario}"
    )

    await ctx.send(mensaje[:1900])


@bot.command()
async def registrar(ctx, *, nombre: str):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)

    datos["personajes"][usuario_id] = {
        "nombre": nombre,
        "oro": datos["personajes"].get(usuario_id, {}).get("oro", 0)
    }

    guardar_bastion(datos)

    await ctx.send(f"✅ {ctx.author.display_name} queda registrado como **{nombre}**.")


@bot.command()
async def oro(ctx):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)
    personaje = obtener_personaje(datos, usuario_id)

    if personaje is None:
        await ctx.send("⛔ Primero registra tu personaje con `!registrar Nombre`.")
        return

    await ctx.send(f"💰 **{personaje['nombre']}** tiene **{personaje['oro']} PO**.")


@bot.command()
async def depositar(ctx, cantidad: int):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)
    personaje = obtener_personaje(datos, usuario_id)

    if personaje is None:
        await ctx.send("⛔ Primero registra tu personaje con `!registrar Nombre`.")
        return

    if cantidad <= 0:
        await ctx.send("⛔ La cantidad debe ser mayor a 0.")
        return

    if personaje["oro"] < cantidad:
        await ctx.send("⛔ No tienes suficiente oro personal.")
        return

    personaje["oro"] -= cantidad
    datos["arcas"] += cantidad

    guardar_bastion(datos)

    await ctx.send(
        f"💰 **{personaje['nombre']}** deposita **{cantidad} PO**.\n\n"
        f"Arcas: **{datos['arcas']} PO**\n"
        f"Oro personal: **{personaje['oro']} PO**"
    )


@bot.command()
async def retirar(ctx, cantidad: int):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)
    personaje = obtener_personaje(datos, usuario_id)

    if personaje is None:
        await ctx.send("⛔ Primero registra tu personaje con `!registrar Nombre`.")
        return

    if cantidad <= 0:
        await ctx.send("⛔ La cantidad debe ser mayor a 0.")
        return

    if datos["arcas"] < cantidad:
        await ctx.send("⛔ Las arcas no tienen suficiente oro.")
        return
    


    datos["arcas"] -= cantidad
    personaje["oro"] += cantidad

    guardar_bastion(datos)

    await ctx.send(
        f"💰 **{personaje['nombre']}** retira **{cantidad} PO**.\n\n"
        f"Arcas: **{datos['arcas']} PO**\n"
        f"Oro personal: **{personaje['oro']} PO**"
    )

@bot.command()
async def actualizardefensores(ctx):
    datos = cargar_bastion()

    datos.setdefault("defensores_detalle", [])

    total = datos.get("defensores", 0)
    registrados_activos = sum(
        1 for d in datos["defensores_detalle"]
        if d.get("estado") == "activo"
    )

    faltan = total - registrados_activos

    if faltan <= 0:
        await ctx.send(
            "🛡️ **Defensores actualizados**\n\n"
            "Todos los defensores activos ya tienen ficha."
        )
        return

    nuevos = []

    for _ in range(faltan):
        defensor = crear_defensor(datos)
        datos["defensores_detalle"].append(defensor)
        nuevos.append(defensor)

    guardar_bastion(datos)

    lineas = []
    for d in nuevos:
        lineas.append(
            f"• **{d['nombre']}** — {d['rol']}\n"
            f"  _{d['historia']}_"
        )

    await ctx.send(
        "🛡️ **Defensores regularizados**\n\n"
        f"Se generaron **{faltan}** fichas para defensores existentes.\n\n"
        + "\n\n".join(lineas)
    )

@bot.command()
async def defensores(ctx):
    datos = cargar_bastion()

    lista = [
        d for d in datos.get("defensores_detalle", [])
        if d.get("estado") == "activo"
    ]

    if not lista:
        await ctx.send(
            "🛡️ **Defensores del bastión**\n\n"
            "No hay defensores activos registrados."
        )
        return

    mensajes = []
    mensaje = (
        "🛡️ **Defensores de la Casa de las Máscaras**\n\n"
        f"Total activo: **{len(lista)}**\n\n"
    )

    for d in lista:
        bloque = (
            f"**{d.get('id', '?')}. {d.get('nombre', 'Defensor sin nombre')}**\n"
            f"Rol: **{d.get('rol', 'Guardia del bastión')}**\n"
            f"Procedencia: **{d.get('procedencia', 'Desconocida')}**\n"
            f"Edad: **{d.get('edad', 'Desconocida')}**\n"
            f"_{d.get('historia', 'Sin historia registrada.')}_\n\n"
        )

        if len(mensaje) + len(bloque) > 1800:
            mensajes.append(mensaje)
            mensaje = ""

        mensaje += bloque

    if mensaje:
        mensajes.append(mensaje)

    for parte in mensajes:
        await ctx.send(parte)

@bot.command()
async def registro(ctx):
    datos = cargar_bastion()

    asalariados = datos.get("asalariados_detalle", [])
    defensores = datos.get("defensores_detalle", [])
    refugiados = datos.get("refugiados")
    husped = datos.get("husped")

    mensaje = "📖 **Registro de la Casa de las Máscaras**\n\n"

    if asalariados:
        mensaje += "👷 **Asalariados**\n"
        for a in asalariados:
            mensaje += (
                f"• **{a.get('id', '?')}. {a.get('nombre', 'Sin nombre')}** "
                f"— {a.get('estado', 'desconocido')}\n"
            )
        mensaje += "\n"

    if defensores:
        mensaje += "🛡️ **Defensores**\n"
        for d in defensores:
            mensaje += (
                f"• **D{d.get('id', '?')}. {d.get('nombre', 'Sin nombre')}** "
                f"— {d.get('estado', 'desconocido')}\n"
            )
        mensaje += "\n"

    if refugiados:
        mensaje += (
            "🏕️ **Refugiados**\n"
            f"• Grupo de **{refugiados.get('cantidad', 0)}** refugiados — presentes\n\n"
        )

    if husped:
        mensaje += (
            "🎭 **Huésped actual**\n"
            f"• **{husped.get('nombre', husped.get('tipo', 'Huésped sin nombre'))}** "
            f"— {husped.get('tipo', 'desconocido')}\n\n"
        )

    if mensaje == "📖 **Registro de la Casa de las Máscaras**\n\n":
        mensaje += "No hay habitantes registrados todavía."

    await ctx.send(mensaje[:1900])

@bot.command()
async def ficha(ctx, identificador: str):
    datos = cargar_bastion()

    registros = []

    for a in datos.get("asalariados_detalle", []):
        item = a.copy()
        item["categoria"] = "asalariado"
        registros.append(item)

    for d in datos.get("defensores_detalle", []):
        item = d.copy()
        item["categoria"] = "defensor"
        registros.append(item)

    if datos.get("husped_detalle"):
        item = datos["husped_detalle"].copy()
        item["categoria"] = "huesped"
        registros.append(item)

    if datos.get("refugiados_detalle"):
        item = datos["refugiados_detalle"].copy()
        item["categoria"] = "refugiados"
        registros.append(item)

    buscado = identificador.lower()

    encontrado = None

    for r in registros:
        nombre = str(r.get("nombre", "")).lower()
        rid = str(r.get("id", ""))

        if buscado == rid or buscado in nombre:
            encontrado = r
            break

    if not encontrado:
        await ctx.send(
            "⛔ **Ficha no encontrada**\n\n"
            "Usa `!registro` para ver los nombres e IDs disponibles."
        )
        return

    categoria = encontrado.get("categoria", "habitante")
    icono = (
        "👷" if categoria == "asalariado"
        else "🛡️" if categoria == "defensor"
        else "🎭" if categoria == "huesped"
        else "🏕️"
)

    oficio_o_rol = encontrado.get("oficio") or encontrado.get("rol") or "Sin función registrada"

    await ctx.send(
        f"{icono} **Ficha de {encontrado.get('nombre', 'Sin nombre')}**\n\n"
        f"**ID:** {encontrado.get('id', '?')}\n"
        f"**Tipo:** {categoria}\n"
        f"**Estado:** {encontrado.get('estado', 'desconocido')}\n"
        f"**Función:** {oficio_o_rol}\n"
        f"**Edad:** {encontrado.get('edad', 'Desconocida')}\n"
        f"**Procedencia:** {encontrado.get('procedencia', 'Desconocida')}\n\n"
        f"**Historia:**\n_{encontrado.get('historia', 'Sin historia registrada.')}_\n\n"
        f"**Motivo de salida:** {encontrado.get('motivo_salida', 'Ninguno')}\n"
        f"**Fecha de salida:** {encontrado.get('fecha_salida', 'Ninguna')}"
    )

@bot.command()
async def despedirasalariado(ctx, identificador: str):
    datos = cargar_bastion()
    buscado = identificador.lower()

    for a in datos.get("asalariados_detalle", []):
        if a.get("estado") != "activo":
            continue

        if buscado == str(a.get("id")) or buscado in a.get("nombre", "").lower():
            a["estado"] = "despedido"
            a["motivo_salida"] = "Despedido del bastión."
            a["fecha_salida"] = str(date.today())
            datos["asalariados"] = max(0, datos.get("asalariados", 0) - 1)

            guardar_bastion(datos)

            await ctx.send(
                "👷 **Asalariado despedido**\n\n"
                f"**{a.get('nombre', 'Sin nombre')}** deja la Casa de las Máscaras.\n"
                f"👷 Asalariados restantes: **{datos['asalariados']}**"
            )
            return

    await ctx.send("⛔ No encontré un asalariado activo con ese ID o nombre.")

@bot.command()
async def despedirdefensor(ctx, identificador: str):
    datos = cargar_bastion()
    buscado = identificador.lower()

    for d in datos.get("defensores_detalle", []):
        if d.get("estado") != "activo":
            continue

        if buscado == str(d.get("id")) or buscado in d.get("nombre", "").lower():
            d["estado"] = "despedido"
            d["motivo_salida"] = "Despedido de la defensa del bastión."
            d["fecha_salida"] = str(date.today())
            datos["defensores"] = max(0, datos.get("defensores", 0) - 1)

            guardar_bastion(datos)

            await ctx.send(
                "🛡️ **Defensor despedido**\n\n"
                f"**{d.get('nombre', 'Sin nombre')}** deja la defensa de la Casa de las Máscaras.\n"
                f"🛡️ Defensores restantes: **{datos['defensores']}/{max_defensores(datos)}**"
            )
            return

    await ctx.send("⛔ No encontré un defensor activo con ese ID o nombre.")

@bot.command()
async def retirarhuesped(ctx):
    datos = cargar_bastion()

    if not datos.get("husped"):
        await ctx.send(
            "🎭 **No hay huésped**\n\n"
            "Actualmente el bastión no hospeda a ningún visitante."
        )
        return

    nombre = datos["husped"].get("nombre", "Huésped sin nombre")

    if datos.get("husped_detalle"):
        datos["husped_detalle"]["estado"] = "retirado"
        datos["husped_detalle"]["fecha_salida"] = str(date.today())
        datos["husped_detalle"]["motivo_salida"] = (
            "Retirado manualmente por el administrador."
        )

    tipo = datos["husped"].get("tipo")

    # Si el huésped ocupaba un puesto temporal, liberarlo.
    if tipo == "mercenario":
        ocupa = datos["husped"].get("ocupa")

        if ocupa == "defensor":
            datos["defensores"] = max(0, datos["defensores"] - 1)

        elif ocupa == "asalariado":
            datos["asalariados"] = max(0, datos["asalariados"] - 1)

    datos.pop("husped", None)

    guardar_bastion(datos)

    await ctx.send(
        "🎭 **Huésped retirado**\n\n"
        f"**{nombre}** ha abandonado la Casa de las Máscaras."
    )

@bot.command()
async def contratardefensor(ctx):
    datos = cargar_bastion()
    costo = 100

    if datos["defensores"] >= max_defensores(datos):
        await ctx.send(
            "⛔ **Contrato imposible**\n\n"
            f"El bastión ya tiene el máximo de defensores: **{max_defensores(datos)}**."
        )
        return

    if datos["arcas"] < costo:
        await ctx.send(
            "⛔ **Contrato imposible**\n\n"
            f"Contratar un defensor cuesta **{costo} PO**, "
            f"pero las arcas solo tienen **{datos['arcas']} PO**."
        )
        return

    nuevo = crear_defensor(datos, origen="contratado")

    datos["arcas"] -= costo
    datos["defensores"] += 1
    datos.setdefault("defensores_detalle", [])
    datos["defensores_detalle"].append(nuevo)

    guardar_bastion(datos)

    await ctx.send(
        "🛡️ **Nuevo defensor contratado**\n\n"
        f"💰 Costo: **{costo} PO**\n"
        f"🏯 Arcas restantes: **{datos['arcas']} PO**\n\n"
        f"**{nuevo['nombre']}**\n"
        f"Rol: **{nuevo['rol']}**\n"
        f"Edad: **{nuevo['edad']}**\n"
        f"Procedencia: **{nuevo['procedencia']}**\n\n"
        f"_{nuevo['historia']}_\n\n"
        f"🛡️ Defensores totales: **{datos['defensores']}/{max_defensores(datos)}**"
    )

@bot.command()
async def agregaroro(ctx, cantidad: int):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)
    personaje = obtener_personaje(datos, usuario_id)

    if personaje is None:
        await ctx.send("⛔ Primero registra tu personaje con `!registrar Nombre`.")
        return

    if cantidad <= 0:
        await ctx.send("⛔ La cantidad debe ser mayor a 0.")
        return

    personaje["oro"] += cantidad
    guardar_bastion(datos)

    await ctx.send(
        f"💰 Se agregan **{cantidad} PO** a **{personaje['nombre']}**.\n"
        f"Oro actual: **{personaje['oro']} PO**"
    )

@bot.command()
async def asalariados(ctx):
    datos = cargar_bastion()

    lista = datos.get("asalariados_detalle", [])

    if not lista:
        await ctx.send(
            "👷 **Asalariados**\n\n"
            "No hay asalariados registrados."
        )
        return

    mensaje = (
        "👷 **Asalariados de la Casa de las Máscaras**\n\n"
        f"Total: **{len(lista)}**\n\n"
    )

    for a in lista:
        estado = "🟢 Activo" if a["estado"] == "activo" else "🔴 Inactivo"

        mensaje += (
            f"**{a['id']}. {a['nombre']}**\n"
            f"🔨 {a['oficio']}\n"
            f"📍 {a['procedencia']}\n"
            f"🎂 {a['edad']} años\n"
            f"{estado}\n"
            f"_{a['historia']}_\n\n"
        )

    await ctx.send(mensaje)

@bot.command()
async def inventario(ctx):
    datos = cargar_bastion()

    inventario = datos.get("inventario", [])

    if not inventario:
        await ctx.send(
            "🎒 **Inventario del bastión**\n\n"
            "El bastión no tiene objetos especiales guardados."
        )
        return

    conteo = {}
    for objeto in inventario:
        conteo[objeto] = conteo.get(objeto, 0) + 1

    lineas = []
    for objeto, cantidad in sorted(conteo.items()):
        if cantidad == 1:
            lineas.append(f"• {objeto}")
        else:
            lineas.append(f"• {objeto} ×{cantidad}")

    await ctx.send(
        "🎒 **Inventario del bastión**\n\n"
        + "\n".join(lineas)
    )

@bot.command()
async def quitaroro(ctx, cantidad: int):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)
    personaje = obtener_personaje(datos, usuario_id)

    if personaje is None:
        await ctx.send("⛔ Primero registra tu personaje con `!registrar Nombre`.")
        return

    if cantidad <= 0:
        await ctx.send("⛔ La cantidad debe ser mayor a 0.")
        return

    if personaje["oro"] < cantidad:
        await ctx.send("⛔ El personaje no tiene suficiente oro.")
        return

    personaje["oro"] -= cantidad
    guardar_bastion(datos)

    await ctx.send(
        f"💰 Se retiran **{cantidad} PO** de **{personaje['nombre']}**.\n"
        f"Oro actual: **{personaje['oro']} PO**"
    )



@bot.command()
async def huerto(ctx):
    datos = cargar_bastion()
    
    if not datos["instalaciones"].get("huerto", False):
        await ctx.send("⛔ El huerto está deshabilitado. Debe repararse antes de producir.")
        return

    if datos.get("evento_pendiente"):
        await ctx.send("⛔ Hay un evento pendiente. Resuélvanlo primero con `!resolver entregar` o `!resolver sobornar`.")
        return
    
    usuario_id = str(ctx.author.id)

    if not puede_actuar(datos, usuario_id):
        await ctx.send(f"⛔ {ctx.author.display_name} ya realizó una acción hoy.")
        return

    multiplicador = calcular_produccion(datos)

    if multiplicador == 0:
        await ctx.send("⛔ El huerto no produjo nada porque no hay asalariados disponibles.")
        return

    resultado = random.randint(1, 4)

    if resultado == 1:
        ganancia = int(100 * multiplicador)
        datos["suministros"] += ganancia
        texto = f"🌾 El huerto produjo comida. **+{ganancia} suministros**."
    elif resultado == 2:
        ganancia = int(5 * multiplicador)
        datos["arcas"] += ganancia
        texto = f"🏮 El huerto produjo plantas decorativas. **+{ganancia} PO a las arcas**."
    elif resultado == 3:
        datos["pociones_curacion"] += 1
        texto = "🧪 El huerto produjo hierbas medicinales. **+1 poción de curación**."
    else:
        datos["venenos"] += 2
        texto = "☠️ El huerto produjo plantas tóxicas. **+2 viales de veneno**."


    registrar_accion(datos, usuario_id)
    mensaje_semana = avanzar_semana(datos)
    guardar_bastion(datos)

    mensaje = f"🌱 **Asalariado trabajó en el huerto.**\n\n{texto}"

    if mensaje_semana:
        mensaje += f"\n\n{mensaje_semana}"

    await ctx.send(mensaje)


@bot.command()
async def almacen(ctx):
    datos = cargar_bastion()
    usuario_id = str(ctx.author.id)

    if not datos["instalaciones"].get("almacen", False):
        await ctx.send("⛔ El almacén está deshabilitado. Debe repararse antes de comerciar.")
        return

    if datos.get("evento_pendiente"):
        await ctx.send("⛔ Hay un evento pendiente. Resuélvanlo primero con `!resolver entregar` o `!resolver sobornar`.")
        return

    if not puede_actuar(datos, usuario_id):
        await ctx.send(f"⛔ {ctx.author.display_name} ya realizó una acción hoy.")
        return

    multiplicador = calcular_produccion(datos)

    if multiplicador == 0:
        await ctx.send("⛔ El almacén no pudo operar porque no hay asalariados disponibles.")
        return

    compra = random.randint(1, 100)

    if compra > datos["arcas"]:
        registrar_accion(datos, usuario_id)
        mensaje_semana = avanzar_semana(datos)
        guardar_bastion(datos)

        mensaje = (
        "📦 **Asalariado intentó trabajar en el almacén.**\n\n"
        f"Mercancía disponible: **{compra} PO**\n"
        f"Arcas actuales: **{datos['arcas']} PO**\n\n"
        "⛔ El asalariado no pudo realizar ningún comercio por falta de oro en las arcas."
    )

        if mensaje_semana:
            mensaje += f"\n\n{mensaje_semana}"

        await ctx.send(mensaje)
        return

    porcentaje = random.randint(5, 10)
    ganancia_base = round(compra * (porcentaje / 100))
    ganancia = int(ganancia_base * multiplicador)
    venta = compra + ganancia

    datos["arcas"] -= compra
    datos["arcas"] += venta

    registrar_accion(datos, usuario_id)
    mensaje_semana = avanzar_semana(datos)
    guardar_bastion(datos)

    mensaje = (
    "📦 **Asalariado trabajó en el almacén.**\n\n"
    f"Mercancía comprada: **{compra} PO**\n"
    f"Beneficio base: **{porcentaje}%**\n"
    f"Ganancia final: **+{ganancia} PO**\n"
    f"Venta total: **{venta} PO**\n\n"
    f"💰 Arcas actuales: **{datos['arcas']} PO**"
)

    if mensaje_semana:
        mensaje += f"\n\n{mensaje_semana}"
    

    await ctx.send(mensaje)

@bot.command()
async def rumor(ctx):
    datos = cargar_bastion()

    try:
        texto = generar_rumor_ia(datos)
    except Exception as error:
        await ctx.send(
            "📜 **Rumor del bastión**\n\n"
            "Un mensajero llegó cubierto de polvo, pero sus palabras se perdieron entre el ruido del camino.\n\n"
            f"`Error: {error}`"
        )
        return

    await ctx.send(
        "📜 **Rumor del bastión**\n\n"
        f"{texto}"
    )

@bot.command()
async def actualizarasalariados(ctx):
    datos = cargar_bastion()

    datos.setdefault("asalariados_detalle", [])
    total = datos.get("asalariados", 0)
    registrados = len(datos["asalariados_detalle"])
    faltan = total - registrados

    if faltan <= 0:
        await ctx.send(
            "👷 **Asalariados actualizados**\n\n"
            "Todos los asalariados activos ya tienen ficha."
        )
        return

    nuevos = []

    for _ in range(faltan):
        asalariado = crear_asalariado(datos)
        datos["asalariados_detalle"].append(asalariado)
        nuevos.append(asalariado)

    guardar_bastion(datos)

    lineas = []
    for a in nuevos:
        lineas.append(
            f"• **{a['nombre']}** — {a['oficio']}\n"
            f"  _{a['historia']}_"
        )

    await ctx.send(
        "👷 **Asalariados regularizados**\n\n"
        f"Se generaron **{faltan}** fichas para asalariados existentes.\n\n"
        + "\n\n".join(lineas)
    )

@bot.command()
async def contratar(ctx):
    datos = cargar_bastion()
    costo = 100

    if datos["arcas"] < costo:
        await ctx.send(
            "⛔ **Contrato imposible**\n\n"
            f"Contratar un asalariado cuesta **{costo} PO**, "
            f"pero las arcas solo tienen **{datos['arcas']} PO**."
        )
        return

    nuevo = crear_asalariado(datos)

    datos["arcas"] -= costo
    datos["asalariados"] += 1
    datos.setdefault("asalariados_detalle", [])
    datos["asalariados_detalle"].append(nuevo)

    guardar_bastion(datos)

    await ctx.send(
        "👷 **Nuevo asalariado contratado**\n\n"
        f"💰 Costo: **{costo} PO**\n"
        f"🏯 Arcas restantes: **{datos['arcas']} PO**\n\n"
        f"**{nuevo['nombre']}**\n"
        f"Oficio: **{nuevo['oficio']}**\n"
        f"Edad: **{nuevo['edad']}**\n"
        f"Procedencia: **{nuevo['procedencia']}**\n\n"
        f"_{nuevo['historia']}_\n\n"
        f"👷 Asalariados totales: **{datos['asalariados']}**"
    )


@bot.command(name="noticia")
async def noticia(ctx):
    await ctx.send("🕯️ Consultando rumores de los Grandes Reinos...")
    try:
        texto = generar_noticia_ia()
        await ctx.send(f"📰 **Diario de los Grandes Reinos**\n\n{texto}")
    except Exception as e:
        await ctx.send(f"⚠️ No pude generar la noticia: {e}")

@bot.command()
async def resolver(ctx, opcion: str):
    datos = cargar_bastion()
    evento = datos.get("evento_pendiente")

    if not evento:
        await ctx.send("⛔ No hay ningún evento pendiente.")
        return

    if evento["tipo"] != "asalariado_criminal":
        await ctx.send("⛔ Este evento pendiente todavía no tiene resolución programada.")
        return

    opcion = opcion.lower()

    if opcion == "entregar":
        entregados = perder_asalariados(
            datos,
            1,
            "Entregado a las autoridades por orden de captura."
        )

        datos["evento_pendiente"] = None
        guardar_bastion(datos)

        await ctx.send(
            "⚖️ **Evento resuelto: Asalariado criminal**\n\n"
            "El asalariado fue entregado a las autoridades.\n"
            "👷 Pierdes **1 asalariado**."
        )
        return

    if opcion == "sobornar":
        costo = random.randint(1, 6) * 100

        if datos["arcas"] < costo:
            await ctx.send(
                "💰 **Soborno imposible**\n\n"
                f"El soborno requerido es de **{costo} PO**, pero las arcas solo tienen **{datos['arcas']} PO**.\n"
                "El evento sigue pendiente."
            )
            return

        datos["arcas"] -= costo
        datos["evento_pendiente"] = None
        guardar_bastion(datos)

        await ctx.send(
            "🤝 **Evento resuelto: Asalariado criminal**\n\n"
            f"Las autoridades aceptan mirar hacia otro lado por **{costo} PO**.\n"
            f"🏯 Arcas restantes: **{datos['arcas']} PO**"
        )
        return

    await ctx.send("⛔ Opción inválida. Usa `!resolver entregar` o `!resolver sobornar`.")

bot.run(TOKEN)
