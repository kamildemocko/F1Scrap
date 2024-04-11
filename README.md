# F1-scrap

## What?
is a simple scrapper utility to download data from formula1.com
I've chosen JSON format as a output format and have structure defined with pydantic for easy parsing

### What data?
Drivers, Circuits, Teams, Results

## How?
First run will download all data, then only results and drivers will update. 


## Where?
This data can be used **by itself**, but I also use it in my other project, **F1 P10 Game**:
```text
https://github.com/kamildemocko/F1P10Game.git
```

## Installation
```commandline
poetry install
poetry run playwright install chromium
poetry run f1_scrap/main.py
```
