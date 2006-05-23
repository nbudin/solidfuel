class ConditionalEvent(Event):
    Cond as Condition

    override def Call(args as (object)) as object:
        if Cond.Status:
            return super(args)
