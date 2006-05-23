class EventGroup(ICallable):
    private _items = []

    Active as bool:
        set:
            _innerSetActive(value, {})

    private def _innerSetActive(value as bool, alreadySet as Boo.Lang.Hash):
        if alreadySet.ContainsKey(self):
            return
        alreadySet[self] = 1
        for item in _items:
            if item isa Event:
                cast(Event, item).Active = value
            elif item isa EventGroup:
                cast(EventGroup, item).Active = value
        

    def Call(args as (object)) as object:
        _innerCall(args, {})
        
    private def _innerCall(args as (object), alreadyCalled as Boo.Lang.Hash):
        if alreadyCalled.ContainsKey(self):
            return
        alreadyCalled[self] = 1
        for item in _items:
            if item isa Event:
                cast(Event, item).Call(args)
            elif item isa EventGroup:
                cast(EventGroup, item).Call(args)

        
    
