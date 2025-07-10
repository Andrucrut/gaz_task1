from py_gpn_kafka.core.config import TopicInfo, BrokerConfig
from py_gpn_kafka.broker.handlers.employee_event_handler import EmployeeEventHandler
from py_gpn_kafka.broker.handlers.employee_create_handler import EmployeeCreateHandler

employee_topic_info = TopicInfo(
    topic_name='employee_events',
    handler_cls=EmployeeEventHandler,
)


broker_config = BrokerConfig(
    topics_info=[employee_topic_info]
)


employee_create_topic_info = TopicInfo(
    topic_name='employee_create_topic',
    handler_cls=EmployeeCreateHandler
)