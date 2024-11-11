import discord
from discord.ext import commands
import json
import random
import variables
import utils

TOKEN = variables.BOT_TOKEN
PREFIX = variables.BOT_PREFIX

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix = PREFIX, intents = intents)

# Load data
def loadData():
    try:
        with open(variables.DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save data
def saveData(data):
    with open(variables.DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Getting players data
players_data = loadData()

# Create new players
def createNewPlayer(name):
    return {
        'name': name,
        'hp': 100,
        'attack': 10,
        'defense': 5,
        'level': 1,
        'experience': 0
    }

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")
    # Sync the commands globally
    await bot.tree.sync()

# PING
@bot.tree.command(name='ping', description='Replies with pong!')
async def ping(interaction: discord.Interaction):
    guildName = interaction.guild.name
    print(f"{variables.DATENOW}       [{guildName}]:{bot.user} = `{PREFIX}ping`")
    await interaction.response.defer()
    await interaction.followup.send('Pong!')

# START
@bot.tree.command(name='start', description='Start a new game!')
async def start_game(interaction: discord.Interaction):
    # Checking player
    player_name = str(interaction.user)
    if player_name in players_data:
        await interaction.response.send_message(f"{interaction.user.mention}, kamu sudah memulai permainan!")
        return

    # Create new player and save it
    players_data[player_name] = createNewPlayer(player_name)
    saveData(players_data)
    await interaction.response.send_message(f"{interaction.user.mention}, permainan dimulai! Selamat datang di dunia RPG!")

# PROFILE
@bot.tree.command(name='profile', description='See your profile and status!')
async def check_status(interaction: discord.Interaction):
    # Profile overview
    player_name = str(interaction.user)
    if player_name not in players_data:
        await interaction.response.send_message(
            f"{interaction.user.mention}, kamu belum memulai permainan! Gunakan `{PREFIX}start` untuk memulai."
        )
        return
    
    player = players_data[player_name]
    embed = discord.Embed(
        title=f"{player['name']}'s Status",
        color=discord.Color.blue()
    )
    embed.add_field(name="❤  HP", value=player['hp'], inline=True)
    embed.add_field(name="⚔  Attack", value=player['attack'], inline=True)
    embed.add_field(name="🛡  Defense", value=player['defense'], inline=True)
    embed.add_field(name="🔗 Level", value=player['level'], inline=True)
    embed.add_field(name="🔷 Experience", value=player['experience'], inline=True)

    await interaction.response.send_message(embed = embed)

# ADVENTURE
@bot.tree.command(name='adventure', description='Go play around and kill nearby monster!')
async def adventure(interaction: discord.Interaction):
    await interaction.response.defer()
    
    chanceGetSkill = random.randint(1, 100)
    player_name = str(interaction.user)

    if player_name not in players_data:
        await interaction.response.send_message(f"{interaction.user.mention}, kamu belum memulai permainan! Gunakan `{PREFIX}start` untuk memulai.")
        return
    
    outcome = random.choice(['success', 'failure', 'treasure'])
    player = players_data[player_name]
    
    if outcome == 'success':
        # Successfully fight, gained exp
        gained_exp = random.randint(10, 30)
        player['experience'] += gained_exp
        message = f"{interaction.user.mention}, petualangan sukses! Kamu mendapatkan **{gained_exp}** EXP."
        
        # Check if level up
        if player['experience'] >= 100:
            player['level'] += 1
            player['experience'] = 0
            player['hp'] += random.randint(20, 50)  # Add hp stat
            message += f" Selamat! Kamu naik ke level **{player['level']}**!"

    elif outcome == 'failure':
        # Unsuccessfully fight, lost less hp
        lost_hp = random.randint(5, 15)
        player['hp'] -= lost_hp
        if player['hp'] < 0:
            player['hp'] = 0
        message = f"{interaction.user.mention}, petualangan gagal. Kamu kehilangan **{lost_hp}** HP. HP kamu sekarang **{player['hp']}**."

    elif outcome == 'treasure':
        # Successfully get treasure
        treasure = random.choice(['Potion', 'Sword', 'Shield'])
        message = f"{interaction.user.mention}, kamu menemukan harta karun dan mendapatkan item: **{treasure}**!"

        # Add item in user inventory
        if 'inventory' not in player:
            player['inventory'] = []
        player['inventory'].append(treasure)
        
    if chanceGetSkill <= 2:
        aiSkill = utils.aiApi("Give 1 unique name skill")
        if 'skills' not in player:
            player['skills'] = []
        player['skills'].append(aiSkill)
        message += f" Keberuntungan berpihak padamu! Kamu mendapatkan skill baru: **{aiSkill}**!"
        
    saveData(players_data)
    await interaction.followup.send(message)
        
if __name__ == '__main__':
    bot.run(TOKEN)