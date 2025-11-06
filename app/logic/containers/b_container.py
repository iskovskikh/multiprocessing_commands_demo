from functools import lru_cache

from punq import Container, Scope

from infra.queue_manager import QueueContainer, QueueManager
from logic.mediator.base import Mediator


@lru_cache(maxsize=1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # services
    container.register(
        QueueContainer,
        factory=QueueManager.get_queue_container,
        scope=Scope.singleton,
    )

    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        # event handlers
        # events

        # command handlers
        # commands

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
