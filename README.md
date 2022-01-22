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

`python marsbots_core/bot.py path/to/json-spec`

### Custom bot

`python ./marsbots/bot.py path/to/json-spec --cog-path='path.to.cog'`
