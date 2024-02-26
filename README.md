# F1-scrap
---
is a simple scrapper utility to download data from f1.com

I chose YAML format as a output format and have defined fields in msgspec for parsing

results.yaml is meant to be run periodically, but not yet set up

## Installation
```commandline
poetry install
poetry run playwright install chromium
```

## Output data
- circuits
- drivers
- teams
- results