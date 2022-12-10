import discord
from discord.ext import commands
import requests
import time
import os
import logging
from bs4 import BeautifulSoup

# Set the logging level to INFO, so that only messages with a severity of INFO or higher will be logged
logging.basicConfig(level=logging.INFO)

# Create a logger that will be used to log messages
logger = logging.getLogger(__name__)

# Create an instance of the Intents class with the default set of privileged intents
intents = discord.Intents.default()

# Create a Discord bot
client = commands.Bot(command_prefix = '!', intents=intents)

# When the bot is ready, print a message to the console
@client.event
async def on_ready():
    print('Bot is ready!')

# When the bot is ready, print a message to the console
@client.event
async def on_ready():
    print('Bot is ready!')

# Define a command that the bot can respond to
@client.command()
async def sports_alert(ctx):

# Process any messages that are sent to the bot
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Process any commands that are sent to the bot
    await client.process_commands(message)
    
    # Define a dictionary that maps league names to their respective ESPN URLs and close game criteria
    leagues = {
        'NFL': {
            'url': 'http://www.espn.com/nfl/scoreboard',
            'is_close': lambda home_score, away_score, time_remaining: abs(int(home_score) - int(away_score)) <= 7 and time_remaining == '4th'
        },
        'NBA': {
            'url': 'http://www.espn.com/nba/scoreboard',
            'is_close': lambda home_score, away_score, time_remaining: abs(int(home_score) - int(away_score)) <= 5 and time_remaining == '4th' and minutes <= 5
        },
        'NCAAF': {
            'url': 'http://www.espn.com/college-football/scoreboard',
            'is_close': lambda home_score, away_score, time_remaining: abs(int(home_score) - int(away_score)) <= 7 and time_remaining == '4th'
        },
        'MLB': {
            'url': 'http://www.espn.com/mlb/scoreboard',
            'is_close': lambda home_score, away_score, time_remaining: abs(int(home_score) - int(away_score)) <= 2 and inning_num >= 8
        },
        'NCAAB': {
            'url': 'http://www.espn.com/mens-college-basketball/scoreboard',
            'is_close': lambda home_score, away_score, time_remaining: abs(int(home_score) - int(away_score)) <= 5 and time_remaining == '4th' and minutes <= 5
        }
    }
    
    # Iterate over the leagues and extract the scores of each game
    for league, info in leagues.items():
        # Use the requests library to fetch the HTML of the ESPN scores page for the league
        response = requests.get(info['url'])

        # Parse the HTML using the BeautifulSoup library
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the elements on the page with the 'scoreboard-container' class
        containers = soup.find_all(class_='scoreboard-container')

        # Iterate over the containers and extract the scores of each game
        for container in containers:
            # Find the home team score
            home_score = container.find(class_='home').find(class_='score').text

            # Find the away team score
            away_score = container.find(class_='away').find(class_='score').text

            # Find the inning of the game (if applicable)
            inning = container.find(class_='inning')
            if inning:
                # Parse the inning to get the number of the current inning
                inning_num = int(inning.text.split(' ')[0])
            else:
                inning_num = None

            # Find the time remaining in the game
            time_remaining = container.find(class_='time-left').text.split(' ')[1]

            # Find the number of minutes remaining in the quarter (if applicable)
            minutes = container.find(class_='time-left').text.split(':')[0]
            if minutes:
                minutes = int(minutes)
            else:
                minutes = None

            # Find the home team name
            home_team = container.find(class_='home').find(class_='team-name').text

            # Find the away team name
            away_team = container.find(class_='away').find(class_='team-name').text
            
            # Check if the game is close according to the criteria for the league
            if info['is_close'](home_score, away_score, time_remaining, inning_num, minutes):
            # Send a message to the Discord channel with the scores of the game
             await ctx.send('Attention. (Game between the {} and {} is close and about to end!)'.format(home_team, away_team))

            # Sleep for 60 seconds
             time.sleep(60)

# Get the Discord bot token from the environment variable
bot_token = os.environ['DISCORD_BOT_TOKEN']

# Run the bot using the Discord bot token
client.run(bot_token)
