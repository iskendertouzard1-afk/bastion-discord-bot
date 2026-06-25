import os
import json
import random
from pathlib import Path
from datetime import date

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
print("TOKEN CARGADO:", os.getenv("DISCORD_TOKEN") is not None)

TOKEN = os.getenv("DISCORD_TOKEN")
ARCHIVO = Path("bastion.json")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


def cargar_bastion():
    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}

    datos.setdefault("arcas", 0)
    datos.setdefault("suministros", 0)
    datos.setdefault("pociones_curacion", 0)
    datos.setdefault("venenos", 0)
    datos.setdefault("acciones_semana", 0)
    datos.setdefault("acciones_diarias", {})
    datos.setdefault("personajes", {})
    datos.setdefault("asalariados", 0)
    datos.setdefault("instalaciones", {
        "huerto":True,
        "almacen":True,
        "armeria": False,
        "bilioteca": False,
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
        "obervatorio": False,
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


def registrar_accion(datos, usuario_id):
    datos["acciones_diarias"][usuario_id] = str(date.today())

def avanzar_semana(datos):
    datos["acciones_semana"] += 1

    if datos["acciones_semana"] < 28:
        return None

    datos["acciones_semana"] = 0

    asalariados = datos["asalariados"]
    salario_total = asalariados

    if asalariados <= 0:
        return "📜 **Fin de semana del bastión**\n\nNo hay asalariados que cobrar salario."

    if datos["arcas"] >= salario_total:
        datos["arcas"] -= salario_total

        return (
            "📜 **Fin de semana del bastión**\n\n"
            f"👷 Asalariados: **{asalariados}**\n"
            f"💰 Salarios pagados: **{salario_total} PO**\n"
            f"🏯 Arcas restantes: **{datos['arcas']} PO**"
        )

    asalariados_pagados = datos["arcas"]
    asalariados_que_se_van = asalariados - asalariados_pagados

    datos["arcas"] = 0
    datos["asalariados"] = asalariados_pagados

    return (
        "📜 **Fin de semana del bastión**\n\n"
        f"💰 Las arcas solo alcanzaron para pagar a **{asalariados_pagados}** asalariados.\n"
        f"🚶 Se marchan **{asalariados_que_se_van}** asalariados por falta de pago.\n"
        f"👷 Asalariados restantes: **{datos['asalariados']}**\n"
        f"🏯 Arcas restantes: **0 PO**"
    )

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command(name="help")
async def ayuda(ctx):
    mensaje = (
        "🏯 **Casa de las Máscaras — Comandos**\n\n"
        "`!estado` — Muestra recursos del bastión.\n"
        "`!registrar Nombre` — Vincula tu Discord con tu personaje.\n"
        "`!oro` — Muestra tu oro personal.\n"
        "`!depositar cantidad` — Deposita oro en las arcas.\n"
        "`!retirar cantidad` — Retira oro de las arcas.\n"
        "`!huerto` — Trabaja el huerto. 1 vez al día.\n"
        "`!almacen` — Trabaja el almacén. 1 vez al día."
        "`!agregaroro cantidad` — Agrega oro a tu personaje.\n"
"`!quitaroro cantidad` — Quita oro a tu personaje.\n"
    )
    await ctx.send(mensaje)


@bot.command()
async def estado(ctx):
    datos = cargar_bastion()

    mensaje = (
        "🏯 **Casa de las Máscaras**\n\n"
        f"💰 Arcas: **{datos['arcas']} PO**\n"
        f"🌾 Suministros: **{datos['suministros']}**\n"
        f"🧪 Pociones de curación: **{datos['pociones_curacion']}**\n"
        f"☠️ Viales de veneno: **{datos['venenos']}**\n"
        f"👷 Asalariados: **{datos['asalariados']}**\n"
    )

    await ctx.send(mensaje)


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


bot.run(TOKEN)