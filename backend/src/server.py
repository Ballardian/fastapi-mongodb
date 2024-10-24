from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
import uvicorn
import motor.motor_asyncio
from pymongo import ReturnDocument

from hcps.routers import router as hcp_router


# Note: sensitive info only included for test purposes - would not include in prod!
DB_NAME = "test_db"
COLLECTION_NAME = "hcp"
MONGODB_URI = "mongodb+srv://georgeballardsoftware:testdb@cluster0.h7jvp.mongodb.net/testdb?retryWrites=true&w=majority&appName=Cluster0"
DEBUG = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan config for FastAPI"""
    # Startup:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
    db = client.test_db
    hcp_collection = db.get_collection(COLLECTION_NAME)

    # Ensure the database is available:
    pong = await db.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    app.hcp_collection = hcp_collection

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()


app = FastAPI(lifespan=lifespan, debug=DEBUG)


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hcp_router, prefix="/api")


@app.get("/")
def read_root():
    """test route"""
    return {"Hello": "World"}


if __name__ == "__main__":
    # uvicorn.run("server:app", host=HOST, port=PORT, reload=DEBUG)
    # Note: for ease use default host/port
    uvicorn.run("server:app", reload=DEBUG)
