from dataclasses import dataclass
from typing import Iterable

from logic.commands.base import CT, CR, CommandHandler
from logic.events.base import ET, EventHandler
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    EventHandlersNotRegisteredException,
)
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator


@dataclass
class Mediator(
    EventMediator[ET],
    CommandMediator[CT, CR],
):
    def register_event(self, event: type[ET], handlers: Iterable[EventHandler[ET]]):
        self.events_map[event].extend(handlers)

    def register_command(self, command: type[CT], handler: CommandHandler[CT, CR]):
        self.commands_map[command].append(handler)

    async def publish(self, events: Iterable[ET]) -> None:
        for event in events:
            event_type = type(event)
            handlers: Iterable[EventHandler] = self.events_map.get(event_type, [])
            if not handlers:
                raise EventHandlersNotRegisteredException(event_type)
            for handler in handlers:
                await handler.handle(event)

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = type(command)
        handlers: Iterable[CommandHandler] = self.commands_map.get(command_type, [])
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        return [await handler.handle(command) for handler in handlers]
