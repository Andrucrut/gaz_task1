from fastapi import FastAPI
from src.api.employee_routes import router as employee_router
from src.api.department_routes import router as department_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


app.include_router(employee_router)
app.include_router(department_router)