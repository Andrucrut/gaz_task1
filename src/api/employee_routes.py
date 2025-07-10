import json
import os
import uuid

from fastapi import APIRouter, Depends
from typing import List
from pg.settings import get_db_manager, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from py_gpn_kafka.broker.messages import MessageOut
from src.models.employee_model import EmployeeCreate, EmployeeRead
from pg.manager import DBManager
from py_gpn_kafka.broker.producer import Producer

router = APIRouter(prefix="/employees", tags=["employees"])
KAFKA_URL = os.environ["KAFKA_URL"]
TOPIC_PREFIX = os.environ["TOPIC_PREFIX"]
EMPLOYEE_EVENTS_TOPIC = f"{TOPIC_PREFIX}_employee_events"


@router.post("/", response_model=EmployeeRead)
async def create_employee(
        employee: EmployeeCreate,
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    created_employee = await repo.add_model(employee)

    event_id = str(uuid.uuid4())
    producer = Producer(connection_url=KAFKA_URL, topic=EMPLOYEE_EVENTS_TOPIC)
    msg = MessageOut(
        key=json.dumps({"id": event_id}).encode("utf-8"),
        value=created_employee.model_dump_json().encode("utf-8"),
        headers=[("event", b"employee_created")]
    )
    await producer.produce_message(msg)

    return created_employee


@router.get("/by_department/{department_id}", response_model=List[EmployeeRead])
async def get_employees_by_department(
        department_id: int,
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    return await repo.get_employees_by_department(department_id)


@router.get("/", response_model=List[EmployeeRead])
async def get_employees(
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    return await repo.get_all()


@router.post("/test-employee-event/")
async def test_employee_event(message: str):
    print(f"[DEBUG] Sending to topic: {EMPLOYEE_EVENTS_TOPIC}")
    producer = Producer(connection_url=KAFKA_URL, topic=EMPLOYEE_EVENTS_TOPIC)

    msg = MessageOut(
        key=json.dumps({"id": str(uuid.uuid4())}).encode("utf-8"),
        value=message.encode("utf-8"),
        headers=[("test", b"1")]
    )

    await producer.produce_message(msg)
    print(f"[DEBUG] Message sent to Kafka: {msg}")
    return {"status": "sent"}

