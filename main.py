from fastapi import FastAPI
from heroic_race_crawler import crawler

api = FastAPI()

@api.get('/laps')
def laps():
    return crawler.getAllLaps()