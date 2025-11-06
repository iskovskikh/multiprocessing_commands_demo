from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Generic, Iterable

from logic.commands.base import CT, CR, CommandHandler


@dataclass(eq=False, kw_only=True)
class CommandMediator(ABC, Generic[CT, CR]):
    commands_map: dict[type[CT], list[CommandHandler[CT, CR]]] = field(
        default_factory=lambda: defaultdict(list),
    )

    @abstractmethod
    def register_command(self, command: type[CT], handlers: Iterable[CommandHandler[CT, CR]]): ...

    @abstractmethod
    def handle_command(self, command: CT) -> Iterable[CR]: ...
