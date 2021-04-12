import discord
from discord.utils import get
import random
from discord.ext import commands
from keep_alive import keep_alive
import os


client = commands.Bot(command_prefix = 'e-')
ROLE = "🔒 | Prigioniero"
TONOR = os.getenv("TONORKEY")


'''
Important commands
'''
# on ready
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game("Hi there👋"))
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
  await ctx.send(f"{extension}.py è stato scaricato")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')


'''
Miscellaneous commands
'''

# ping
@client.command(name='ping', aliases=['pong'])
@commands.has_permissions(manage_guild=True)
async def ping(ctx):
  await ctx.send(f"WoW captain, we're fast af: {round(client.latency * 1000)}ms")

# dm users
@client.command()
@commands.has_permissions(manage_guild=True)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await client.fetch_user(user_id)
            await target.send(args)
            await ctx.message.delete()
            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Couldn't dm the given user.")
        

    else:
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
  await member.ban(reason=reason)
  await ctx.send(f"{member.mention} banned as you wished.")

# unban
@client.command(name='unban', aliases=['unbanuser'])
@commands.has_permissions(manage_guild=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")
  for ban_entry in banned_users:
    user = ban_entry.user

    if(user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"{user.mention} unbanned as you wished.")
      return

# add Prigioniero
@client.command(pass_context=True) # Adds a role, you can change the role by changing the variable ROLE at the top
@commands.has_permissions(manage_guild=True)
async def prigione(ctx, member:discord.Member):
  role = discord.utils.get(member.guild.roles, name = "🔒 | Prigioniero")
  await ctx.message.delete()
  await member.add_roles(role)
  embed = discord.Embed(title='Guardie', color = 0xe67e22)
  embed.add_field(name=f'{member}', value=f'{member.mention} è stato buttato nel gabbio!')
  embed.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn4.iconfinder.com%2Fdata%2Ficons%2Fwhsr-january-flaticon-set%2F512%2Flock.png&f=1&nofb=1')
  await ctx.send(embed=embed)

# remove Prigioniero
@client.command(pass_context=True) # Removes a role, you can change the role by changing the variable ROLE at the top
@commands.has_permissions(manage_guild=True)
async def scarcera(ctx, member: discord.Member):
  role = discord.utils.get(member.guild.roles, name = "🔒 | Prigioniero")
  await ctx.message.delete()
  await member.remove_roles(role)
  embed = discord.Embed(title='Guardie', color = 0x3498db)
  embed.add_field(name=f'{member}', value=f'{member.mention} è stato scarcerato!')
  embed.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn4.iconfinder.com%2Fdata%2Ficons%2Fwhsr-january-flaticon-set%2F512%2Flock.png&f=1&nofb=1')
  await ctx.send(embed=embed)

'''
Fun
'''

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
  embed = discord.Embed(title="Magic Ball")
  embed.add_field(name=f'{ctx.author.name}', value=f'Ha chiesto {question}')
  embed.add_field(name='Risposta:', value = f'{random.choice(responses)}')
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


# runs bot
client.run(os.getenv("TOKEN"))