from py_gpn_kafka.broker.handlers import BaseHandler
import logging
from pydantic import BaseModel


class EmployeeCreateResponse(BaseModel):
    message: str


class EmployeeCreateHandler(BaseHandler):
    async def process_business_logic(self, input_bytes: bytes):
        msg = input_bytes.decode('utf-8')
        print(f"!!! HANDLER TRIGGERED !!!: {msg}")
        logging.warning(f"!!! HANDLER TRIGGERED !!!: {msg}")
        return  EmployeeCreateResponse(message=msg)

