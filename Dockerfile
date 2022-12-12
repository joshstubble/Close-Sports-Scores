FROM python:3.8

# Install the required packages
RUN pip install discord requests beautifulsoup4

# Copy the code to the container
COPY . /app
WORKDIR /app

# Run the bot
CMD ["python", "bot.py"]