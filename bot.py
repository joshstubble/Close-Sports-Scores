import discord
from discord.ext import commands
import requests
import time
import os

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def sports_alert(ctx):
    # Get the Discord bot token from the environment variable
    bot_token = os.environ['DISCORD_BOT_TOKEN']

    # Get the theScore API key from the environment variable
    api_key = os.environ['THESCORE_API_KEY']
    
    # Use the requests library to fetch information about MLB games
    mlb_games = requests.get('https://api.thescore.com/mlb/events', headers={'Authorization': f'Bearer {api_key}'})
   
   # Use the requests library to fetch information about NBA games
    nba_games = requests.get('https://api.thescore.com/nba/events', headers={'Authorization': f'Bearer {api_key}'})

    # Use the requests library to fetch information about NFL games
    nfl_games = requests.get('https://api.thescore.com/nfl/events', headers={'Authorization': f'Bearer {api_key}'})
    
    # Use the requests library to fetch information about NCAAF games
    ncaaf_games = requests.get('https://api.thescore.com/ncaaf/events', headers={'Authorization': f'Bearer {api_key}'})
    
    # Use the requests library to fetch information about NCAAB games
    ncaab_games = requests.get('https://api.thescore.com/ncaab/events', headers={'Authorization': f'Bearer {api_key}'})

    while True:
        # Iterate over the list of NBA games and check if any are close and near the end
        for game in nba_games:
            if game['score_difference'] < 5 and game['time_remaining'] < 120:
                await ctx.send(f'Attention! The {game["home_team"]} vs {game["away_team"]} game is close and about to end!')

        # Iterate over the list of NFL games and check if any are close and near the end
        for game in nfl_games:
            if game['score_difference'] < 5 and game['time_remaining'] < 120:
                await ctx.send(f'Attention! The {game["home_team"]} vs {game["away_team"]} game is close and about to end!')
                
          # Iterate over the list of MLB games and check if any are close and near the end
        for game in mlb_games:
            if game['score_difference'] < 5 and game['time_remaining'] < 120:
                await ctx.send(f'Attention! The {game["home_team"]} vs {game["away_team"]} game is close and about to end!')
        
          # Iterate over the list of NCAAB games and check if any are close and near the end
        for game in ncaab_games:
            if game['score_difference'] < 5 and game['time_remaining'] < 120:
                await ctx.send(f'Attention! The {game["home_team"]} vs {game["away_team"]} game is close and about to end!')
          
          # Iterate over the list of NCAAB games and check if any are close and near the end
        for game in ncaaf_games:
            if game['score_difference'] < 5 and game['time_remaining'] < 120:
                await ctx.send(f'Attention! The {game["home_team"]} vs {game["away_team"]} game is close and about to end!')

        # Sleep for 60 seconds
        time.sleep(60)

client.run(bot_token)
