# Mars College Discord Bots Framework

This repository contains code for creating chatbots/utility bots for Mars College, or otherwise.

There are several useful utilities for chat programs, including support for numerous language model API providers, as well as methods for completing text, searching topics, and getting message similarity.

## Setup (for development)

```
python -m virtualenv venv
pip install flit
flit install --deps=all --pth-file
```

## Creating a bot

All bots must be placed in a directory equal to or higher in the file system than the run script (`bot.py`). It is recommended that you create a folder called `bots` in the `marsbots-core` directory, then create additional folders and files in there as needed.

All bots expect three things:

- A JSON settings file
- A Python script containing the bot's code as a Discord.py Cog class
- A .env file to load API keys/settings from

### Settings File

The bot's JSON settings file should contain the following:

`"name"`: The name of the bot
`"token_env"`: The name of the environment variable which contains the discord bot token used to run the bot
(Optional) `"command_prefix"`: This will be the prefix used for the bot to respond to commands.

### Cog File

The bot's main logic should be created as a Discord.py Cog class, and should have a setup function which adds the Cog to the bot.

### Env File

This should contain any API keys or sensitive variables you need to use to run the bot. Expected default names for environment variables can be found in the `config.py` file of Marsbots core.

## Running Your Bot

### Locally

Bots can be run locally using a command such as the following:

```bash
python bot.py ./examples/examplebot/examplebot.json --cog-path=examples.examplebot.examplebot --dotenv-path=.env
```

Note that the `--cog-path` flag should be provided using python module syntax, using dots.

### Managing several bots with PM2

Several bots can be managed at once using [PM2](https://pm2.keymetrics.io/) and a PM2 config file. An example config file is provided in the `examples` folder for running the example bot using PM2.
