import discord
from discord.utils import get
import random
from discord.ext import commands
from keep_alive import keep_alive
from discord.ext.commands import MissingPermissions
import os

# Bot prefix
client = commands.Bot(command_prefix = 'e-')
# Add/remove role
ROLE = "🔒 | Prigioniero"
# Tonor API key
TONOR = os.getenv("TONORKEY")


'''
Important commands
'''
# on ready
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game("Hi there👋"))
  # online output
  print("Logged in as {0.user}".format(client))

# removing default help command
client.remove_command('help')

# 1h live server
keep_alive()

# load cogs
@client.command(name="loadcogs", aliases=["lc", "loadc", "lcogs"])
@commands.has_role("🌐 Owner")
async def loadcogs(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"{extension}.py è stato caricato")

# unload cogs
@client.command(name="unloadcogs", aliases=["uc", "unloadc", "ucogs"])
@commands.has_role("🌐 Owner")
async def unloadcogs(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  print(f"{extension}.py has been succesfully unloaded")
  await ctx.send(f"{extension}.py has been succesfully unloaded")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
  
# error handler
@client.event
async def on_command_error(ctx, error):
    pass

'''
Miscellaneous commands
'''

# broadcast
@client.command(name="broadcast", aliases=["announce", "bc"])
@commands.has_role("🌐 Owner")
async def broadcast(ctx, *, announce):
  embed = discord.Embed(title="Admin broadcast", description=f'{announce}', color=discord.Color.red())
  embed.set_author(name=f'{ctx.message.author}')
  await ctx.message.delete()
  await ctx.send(embed=embed)
  print(f"sent broadcast to {ctx.message.channel} by {ctx.author}")

# source
@client.command(name="source", aliases=["sorgente"])
async def sourceLink(ctx):
  await ctx.send(f"Our source code is available at https://github.com/UnTizioCheEsiste/eNerdsBot\n@2021 UnTizioCheEsiste, PhaseLocked")
  print(f"Repository link shown")

# sauce
@client.command(name="sauce", aliases=["zozzerie", "porn"])
async def sauce(ctx):
  await ctx.message.delete()
  await ctx.send(f"https://www.youtube.com/watch?v=xxhNCY21-xs")
  await ctx.send(f"Hey @everyone ! {ctx.message.author.mention} tried to obtain porn material")

# ping
@client.command(name='ping', aliases=['pong'])
@commands.has_permissions(manage_guild=True)
async def ping(ctx):
  # printing ping
  await ctx.send(f"WoW captain, we're fast af: {round(client.latency * 1000)}ms")

# dm users
@client.command()
@commands.has_permissions(manage_guild=True)
async def dm(ctx, user_id=None, *, args=None):
  # if there is userID and args
    if user_id != None and args != None:
        try:
            target = await client.fetch_user(user_id)
            await target.send(args)
            await ctx.message.delete()
            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
          # userID not given
            await ctx.channel.send("Couldn't dm the given user.")
        
    else:
      # userID or message not given
        await ctx.channel.send("You didn't provide a user's id and/or a message.")

# help
@client.command(name='help')
async def help(ctx):
  embed = discord.Embed(title="Help:")
  embed.add_field(name='site', value='https://eNerdsBot.untiziocheesi.repl.cov', inline=False)
  embed.set_author(name="UnTizioCheEsiste", icon_url="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fimg1.wikia.nocookie.net%2F__cb20100126212215%2Fconearth%2Fimages%2F7%2F79%2FHelp_icon.png&f=1&nofb=1")
  embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.onlinewebfonts.com%2Fsvg%2Fimg_210092.png&f=1&nofb=1")
  author = ctx.message.author
  await author.send(embed=embed)
  await ctx.message.delete()


'''
Moderation commands
'''

# kick
@client.command(name='kick')
@commands.has_permissions(manage_guild=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked')

# ban
@client.command(name='ban', aliases=['banhammer', 'banuser'])
@commands.has_permissions(manage_guild=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  try:
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} banned as you wished.")
  except:
    await ctx.send(f'Missing username!')
    print("Ban ha avuto problemi, mancato username")

# unban
@client.command(name='unban', aliases=['unbanuser'])
@commands.has_permissions(manage_guild=True)
async def unban(ctx, *, member):
  try:
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
      user = ban_entry.user

      if(user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user.mention} unbanned as you wished.")
        return
  except:
    await ctx.send(f'Missing username!')
    print("Unban ha avuto problemi, mancato username")

# add Prigioniero
@client.command(pass_context=True) # Adds a role, you can change the role by changing the variable name
@commands.has_permissions(manage_guild=True)
async def prigione(ctx, member:discord.Member):
  try:
    role = discord.utils.get(member.guild.roles, name = "🔒 | Prigioniero")
    await ctx.message.delete()
    await member.add_roles(role)
    embed = discord.Embed(title='Guardie', color = 0xe67e22)
    embed.add_field(name=f'{member}', value=f'{member.mention} è stato buttato nel gabbio!')
    embed.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn4.iconfinder.com%2Fdata%2Ficons%2Fwhsr-january-flaticon-set%2F512%2Flock.png&f=1&nofb=1')
    await ctx.send(embed=embed)
  except:
    await ctx.send(f'Missing username!')
    print("Prigione ha avuto problemi, mancato username")

# remove Prigioniero
@client.command(pass_context=True) # Removes a role, you can change the role by changing the variable name
@commands.has_permissions(manage_guild=True)
async def scarcera(ctx, member: discord.Member):
  try:
    role = discord.utils.get(member.guild.roles, name = "🔒 | Prigioniero")
    await ctx.message.delete()
    await member.remove_roles(role)
    embed = discord.Embed(title='Guardie', color = 0x3498db)
    embed.add_field(name=f'{member}', value=f'{member.mention} è stato scarcerato!')
    embed.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn4.iconfinder.com%2Fdata%2Ficons%2Fwhsr-january-flaticon-set%2F512%2Flock.png&f=1&nofb=1')
    await ctx.send(embed=embed)
  except:
    await ctx.send(f'Missing username!')
    print("Scarcera ha avuto problemi, mancato username")

# clear
@client.command(pass_context=True, name="clear", aliases=["c", "cl"])
@commands.has_permissions(manage_guild=True)
async def clear(ctx, limit: int):
  try:
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    nm=limit
    print(f"{ctx.author} deleted {nm} messages in the channel {ctx.channel}")
  except:
    limit = 5
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    nm=limit
    print(f"{ctx.author} deleted {nm} messages in the channel {ctx.channel}")

# provvedimenti
@client.command(name="provvedimento", aliases=["prov"])
@commands.has_role("🌐 Owner")
async def provvedimenti(ctx, data,  *, announce):
  embed = discord.Embed(title=f'Provvedimento del {data}', description=f'{ctx.message.author}: {announce}', color=discord.Color.red())
  await ctx.message.delete()
  await ctx.send(embed=embed)
  print(f"sent provv to {ctx.message.channel} by {ctx.author}")

'''
Fun
'''
# prof insults
@client.command(name="profinsult", aliases=["pinsult", "profi", "pi"])
async def profinsult(ctx, name, *, insults):
  embed=discord.Embed(title="InsultiBot", color = discord.Color.red())
  embed.add_field(name=f'{ctx.message.author}', value=f'{name} {insults}')
  await ctx.message.delete()
  await ctx.send(embed=embed)

# programmer
@client.command(name="programmer", aliases=["programmatore"])
@commands.has_role("⌨Programmer")
async def programmer(ctx, *, language):
  embed = discord.Embed(title="Another lazy programmer", description=f'{ctx.author.mention} tried to shot himself after {random.randint(2, 7)} hours of {language}', color=discord.Color.green())
  await ctx.message.delete()
  await ctx.send(embed=embed)

# eightball
@client.command(pass_context=True, name="eightball", aliases=["8ball", "eball"])
async def eightball(ctx, *, question):
  responses = ["100%.",                               # responses: You can change with whatever you want
                "Senza dubbio.",
                "Assolutamente.",
                "Puoi contarci, o almeno penso.",
                "Per come la vedo io, si.",
                "Molto probabile.",
                "Me pare de si.",
                "Sì.",
                "Chiedimelo dopo.",
                "Meglio se non ne parliamo...",
                "Idk man, carpe diem.",
                "Usa i tuoi pochi neuroni e richiedi la domanda.",
                "Non ci contare nibba.",
                "AHAHAHHAHA, No.",
                "Le mie risorse rilevano cazzata.",
                "Me sa proprio de no.",
                "Assolutamente no, nebro."]
  r = random.choice(responses)
  embed = discord.Embed(title="Magic Ball")
  embed.add_field(name=f'{ctx.author.name}', value=f'Ha chiesto {question}')
  embed.add_field(name='Risposta:', value = f'{r}')
  await ctx.message.delete()
  await ctx.send(embed=embed)

# avatar competition
@client.command(pass_context=True, name="avatarcompetition", aliases=["ac", "avatarc", "acompetition"]) 
@commands.has_role("🏆 | Competition Master")# You can chage this role
async def avatarcompetition(ctx, *, member: discord.Member = None):
  if not member:
    member = ctx.message.author
  judge = [ "10/10",
            "9/10",
            "8/10",
            "8/10",
            "8/10",
            "8/10",
            "8/10",
            "7/10",
            "7/10",
            "7/10",
            "7/10",
            "7/10",
            "6/10",
            "6/10",
            "6/10",
            "6/10",
            "5/10",
            "5/10",
            "4/10",
            "4/10",
            "3/10",
            "3/10",
            "3/10",
            "2/10",
            "2/10",
            "1/10",
            "1/10",
            "0/10"]
  userAvatar = member.avatar_url
  embed = discord.Embed(title=f"**{member}'s avatar**")
  embed.add_field(name="Voto", value=f"{random.choice(judge)}")
  embed.set_image(url=userAvatar)
  await ctx.message.delete()
  await ctx.send(embed=embed)

# possessore cp
@client.command(pass_context=True, name="childporn", aliases=["cp", "childp"]) 
@commands.has_permissions(manage_guild=True)
async def cposs(ctx, member:discord.Member):
  role = discord.utils.get(member.guild.roles, name = "🔞Possessore di CP🔞")
  await ctx.message.delete()
  await member.add_roles(role)
  embed = discord.Embed(title='Guardie', color = 0xe67e22)
  embed.add_field(name=f'{member}', value=f'{member.mention} è un possessore di cp!!')
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/646007605826682901/831883402297868349/cp.png')
  await ctx.send(embed=embed)

'''
Error Handling
'''
@client.event
async def on_command_error(ctx, error):
  embed = discord.Embed(title="Errore")
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.delete()
    embed.add_field(name="Argomento", value="Non hai inserito tutti gli argomenti obbligatori!")
    await ctx.send(embed=embed)
  elif isinstance(error, commands.MissingPermissions):
    await ctx.message.delete()
    embed.add_field(name="Permesso", value="Non hai i permessi necessari per farlo!")
    await ctx.send(embed=embed)
  else:
    raise error
  

# runs bot
client.run(os.getenv("TOKEN"))

# Discord.py Bot@2021 UnTizioCheEsiste, PhaseLocked
# GNU GPLv3 License©