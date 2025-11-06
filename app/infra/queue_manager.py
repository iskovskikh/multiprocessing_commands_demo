import logging
from dataclasses import dataclass
from multiprocessing import Manager, Queue

logger = logging.getLogger(__name__)


@dataclass
class QueueContainer:
    command_queue: Queue
    command_result_queue: Queue


class QueueManager:
    queue_container: QueueContainer | None = None

    @classmethod
    def init_queue_container(cls):
        if cls.queue_container is None:
            manager = Manager()
            cls.queue_container = QueueContainer(
                command_queue=manager.Queue(), command_result_queue=manager.Queue()
            )
        else:
            raise RuntimeError("QueueManager уже установлен!")

    @classmethod
    def set_queue_container(cls, container: QueueContainer):
        if cls.queue_container is None:
            cls.queue_container = container
        else:
            raise RuntimeError("QueueManager уже установлен!")

    @classmethod
    def get_queue_container(cls) -> QueueContainer:
        if cls.queue_container is None:
            raise RuntimeError("QueueManager еще не установлен!")
        else:
            return cls.queue_container
