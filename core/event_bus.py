from collections import defaultdict


class EventBus:

    def __init__(self):
        self._events = defaultdict(list)

    def subscribe(self, event_name, callback):
        self._events[event_name].append(callback)

    def emit(self, event_name, *args, **kwargs):

        for callback in self._events[event_name]:
            callback(*args, **kwargs)


event_bus = EventBus()