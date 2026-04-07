import os, uvicorn
from fastapi import FastAPI
from src.controllers import userControllers, cardControllers, authControllers
from fastapi.middleware.cors import CORSMiddleware
from src.database import create_database

app = FastAPI(title="PokeTreiner", description="An Pokemon Card Social Midia API")

@app.get('/')
async def root():
    return {'mensagem' : 'API TEST OK'}

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- ROUTERS ---- 
app.include_router(userControllers.router)
app.include_router(authControllers.router)
app.include_router(cardControllers.router)


# ---- MAIN ----
if __name__ == '__main__':
    create_database()
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)