from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.routes import channel, playlist
from utils.security import get_api_key


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(playlist, dependencies=[Depends(get_api_key)])

app.include_router(channel, dependencies=[Depends(get_api_key)])
# app.add_api_route("playlist", endpoint=playlist)
