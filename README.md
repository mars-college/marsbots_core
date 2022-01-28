# Mars College Discord Bots

Makin' bots

## Setup

```
python -m virtualenv venv
pip install flit
flit install --pth-file
```

## Running Bots

### Simple bot (from json)

`python bot.py path/to/json-spec`

### Custom bot

`python bot.py path/to/json-spec --cog-path=path.to.cog --dotenv-file=path/to/.env`
