import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/slow-async")  # ❌ sleep bloquant DANS un async def
async def slow_async():
    time.sleep(5)  # gèle l'event loop pendant 5s
    return {"route": "slow-async"}


@app.get("/slow-sync")  # ✅ sleep bloquant DANS un def
def slow_sync():
    time.sleep(5)  # tourne chez un commis → ne gèle rien d'autre
    return {"route": "slow-sync"}


@app.get("/ping")  # endpoint rapide, pour tester la réactivité
async def ping():
    return {"pong": True}
