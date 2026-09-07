"""In-memory and pub/sub async event broadcaster for trading events."""

import asyncio
from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], Any]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Any]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def emit(self, event_type: str, data: Dict[str, Any]):
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Error executing handler for {event_type}: {e}")


# Singleton application event bus
event_bus = EventBus()
