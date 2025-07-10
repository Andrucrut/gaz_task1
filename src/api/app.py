import asyncio

from fastapi import FastAPI
from src.api.employee_routes import router as employee_router
from src.api.department_routes import router as department_router
from src.api.project_routes import router as project_router
from py_gpn_kafka import build_kafka_app
from py_gpn_kafka.kafka_config import broker_config
import asyncio

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.on_event("startup")
async def startup():
    print("=== STARTUP: launching kafka_app ===")
    kafka_app = build_kafka_app(broker_config)
    asyncio.create_task(kafka_app.start())
    print("=== STARTUP: kafka_app launched ===")



app.include_router(employee_router)
app.include_router(department_router)
app.include_router(project_router)