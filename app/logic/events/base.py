from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic


@dataclass(frozen=True)
class BaseEvent: ...


ET = TypeVar("ET", bound=BaseEvent)


@dataclass(frozen=True)
class EventHandler(ABC, Generic[ET]):
    @abstractmethod
    async def handle(self, event: ET) -> None: ...
