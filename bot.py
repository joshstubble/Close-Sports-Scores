import discord
from discord.ext import commands
import requests
import time
import os
import logging
from bs4 import BeautifulSoup

# Set the logging level to INFO, so that only messages with a severity of INFO or higher will be logged
logging.basicConfig(level=logging.DEBUG)

# Create a logger that will be used to log messages
logger = logging.getLogger(__name__)

# Create an instance of the Intents class with the messages intent enabled
intents = discord.Intents(messages=True)

# Create a Discord bot
client = commands.Bot(command_prefix = '!', intents=intents)

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

@client.event
async def on_ready():
    # Log the "Bot is ready!" message using the logger object
    logger.info('Bot is ready!')

@client.command()
async def startscores(ctx):
    # Get the channel object that the message was sent in
    channel = ctx.channel

    # Send a confirmation message
    await channel.send('The `startscores` command has been received. The bot will now start sending messages.')

    # Use a while loop to keep sending messages until the `!stopscores` command is received
    while True:
        # Get the latest messages sent in the channel
        messages = []
        async for message in channel.history(limit=1):
            messages.append(message)

        # Get the most recent message
        message = messages[0]

        # Check if the `!stopscores` command has been received
        if message.content == '!stopscores':
            break

        # Fetch the latest scores from the ESPN website
        url = 'http://www.espn.com/nfl/scoreboard'
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the home and away scores for the first game on the scoreboard
        home_team_score_element = soup.select_one('.Scoreboard__Column flex-auto Scoreboard__Column--1 Scoreboard__Column--Score')
        away_team_score_element = soup.select_one('.Scoreboard__Column flex-auto Scoreboard__Column--1 Scoreboard__Column--Score')
        home_score = home_team_score_element.text
        away_score = away_team_score_element.text

        # Find the time remaining in the first game on the scoreboard
        time_remaining_element = soup.select_one('.game-status .time-remaining')
        time_remaining = time_remaining_element.text

        # Check if any games are close
        is_close = False
        for league_name, league_info in leagues.items():
            # Use the `is_close()` method to determine whether the game is close
            if league_info['is_close'](home_score, away_score, time_remaining):
                is_close = True
                break

        # If a close game was found, send a message
        if is_close:
            await channel.send('A close game was found!')

        # Sleep for a few seconds before checking for close games again
        time.sleep(5)



# Define a command that the bot can respond to
@client.command()
async def sports_alert(ctx, *league_names):
    # Iterate over the league names and extract the scores for each league
    for league_name in league_names:
        # Get the info for the league from the `leagues` dictionary
        league_info = leagues[league_name]

        # Use the requests library to fetch the HTML of the ESPN scores page for the league
        response = requests.get(league_info['url'])

    # Parse the HTML using the BeautifulSoup library
    soup = BeautifulSoup(response.text, 'html.parser')
    # Print the parsed HTML to the console
    print(soup.prettify())

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
