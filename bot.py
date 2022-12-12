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

@client.event
async def on_ready():
    # Indented code goes here
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!startscores'):
        # Get the channel object that the message was sent in
        channel = message.channel

        # Use a while loop to keep sending messages until the `!stopscores` command is received
        while True:
            # Check if the `!stopscores` command has been received
            if message.content == '!stopscores':
                break

            # Use the `send()` method to send a message to the channel
            await channel.send('This is an example of a message that the bot would send')

            # Sleep for a few seconds before sending the next message
            time.sleep(5)

# Define a command that the bot can respond to
@client.command()
async def sports_alert(ctx):
    # Indented code goes here
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
@client.command()
async def sports_alert(ctx, leagues):
    # Iterate over the leagues and extract the scores of each game
    for league, info in leagues.items():
    # Use the requests library to fetch the HTML of the ESPN scores page for the league
        response = requests.get(info['url'])
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
        # Find the minutes remaining in the game
        minutes = container.find(class_='minutes').text
        
        # Find the inning number
        innings = container.find(class_='innings').text
        
        # Find the home team score
        home_score = container.find(class_='home').find(class_='score').text

        # Find the away team score
        away_score = container.find(class_='away').find(class_='score').text

        # Find the time remaining in the game
        time_remaining = container.find(class_='time-remaining').text

        # Check if the game is considered "close" based on the criteria defined in the `leagues` dictionary
        if info['is_close'](home_score, away_score, time_remaining):
            # If the game is close, send a message to the channel with the teams and scores
            await ctx.send(f"{league}: {home_score} - {away_score}")


# Get the Discord bot token from the environment variable
bot_token = os.environ['DISCORD_BOT_TOKEN']

# Run the bot using the Discord bot token
client.run(bot_token)