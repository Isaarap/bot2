import discord
from discord.ext import commands, tasks
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de cliente de Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Conexión a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Comando de inicio para el bot
@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión en Discord.')
    await bot.change_presence(activity=discord.Game(name="Gestionando fichajes"))

# Comando de ejemplo para ver las horas trabajadas
@bot.command(name='horas')
async def horas(ctx):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT nombre, horas_trabajadas FROM fichajes ORDER BY horas_trabajadas DESC LIMIT 5")
    result = cursor.fetchall()
    mensaje = "Top 5 horas trabajadas:\n"
    for row in result:
        mensaje += f"{row[0]}: {row[1]} horas\n"
    await ctx.send(mensaje)
    db.close()

# Comando para iniciar fichaje
@bot.command(name='iniciar_fichaje')
async def iniciar_fichaje(ctx):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO fichajes (nombre, horas_trabajadas) VALUES ('{ctx.author.name}', 0)")
    db.commit()
    await ctx.send(f"{ctx.author.name} ha iniciado el fichaje.")
    db.close()

# Comando para finalizar fichaje
@bot.command(name='finalizar_fichaje')
async def finalizar_fichaje(ctx):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE fichajes SET horas_trabajadas = horas_trabajadas + 1 WHERE nombre = '{ctx.author.name}'")
    db.commit()
    await ctx.send(f"{ctx.author.name} ha finalizado su fichaje.")
    db.close()

# Iniciar el bot
bot.run(os.getenv("BOT_TOKEN"))
