import uvicorn
from fastapi import FastAPI

from app.routers.tables_router import tables_router
from app.routers.reserv_router import reservation_router


app = FastAPI()

# Подключение роутеров
app.include_router(tables_router)
app.include_router(reservation_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
