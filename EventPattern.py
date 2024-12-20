class EventSubscriber:
    subscribers = {}
    
    @classmethod
    def subscribe(cls, event_type, function):
        if not event_type in cls.subscribers:
            cls.subscribers[event_type] = []
        cls.subscribers[event_type].append(function)
        
    @classmethod
    def unsubscribe(cls, event_type, function):
        if not event_type in cls.subscribers:
            assert "Cannot remove events that dont exist"
        cls.subscribers[event_type].remove(function)
        
    @classmethod
    def notify(cls, event_type, **kwargs):
        if not event_type in cls.subscribers:
            assert "Trying to call event with no subscibers"
        for function in cls.subscribers[event_type]:
            function(**kwargs)