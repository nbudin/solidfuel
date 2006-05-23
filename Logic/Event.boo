class Event(ICallable):
    callable EventResponder(sender)
    callable VoidEventResponder() as System.Void
    private event _Trigger as EventResponder
    private event _TriggerVoid as VoidEventResponder

    public Args as (object)
    public Active as bool = true

    static def op_Addition(evt as Event, resp as EventResponder):
        evt._Trigger += resp
        return evt

    static def op_Addition(evt as Event, resp as VoidEventResponder):
        evt._TriggerVoid += resp
        return evt

    static def opt_Subtraction(evt as Event, resp as EventResponder):
        evt._Trigger -= resp
        return evt

    static def op_Subtraction(evt as Event, resp as VoidEventResponder):
        evt._TriggerVoid -= resp
        return evt

    def Call(args as (object)) as object:
        if Active:
            Args = args
            _Trigger(self)
            _TriggerVoid()
