from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.job import router as JobRouter
from server.routes.direction import router as DirectionRouter
from server.routes.field import router as FieldRouter

app = FastAPI()

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

app.include_router(JobRouter, tags=["Job"], prefix="/jobs")
app.include_router(DirectionRouter, tags=["Direction"], prefix="/directions")
app.include_router(FieldRouter, tags=["Field model (clustering)"], prefix="/fields")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}