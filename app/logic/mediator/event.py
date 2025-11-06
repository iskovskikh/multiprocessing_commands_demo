from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generic, Iterable

from logic.events.base import ET, EventHandler


@dataclass(eq=False, kw_only=True)
class EventMediator(ABC, Generic[ET]):
    events_map: dict[ET, list[EventHandler[ET]]] = field(
        default_factory=lambda: defaultdict(list),
    )

    @abstractmethod
    def register_event(self, event: type[ET], handlers: Iterable[EventHandler[ET]]): ...

    async def publish(self, events: Iterable[ET]): ...
