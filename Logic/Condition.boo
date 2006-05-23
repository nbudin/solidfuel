import System

class Condition:
    Changed as Event = Event()

    callable PollFunction() as bool
    private _pollFunc as PollFunction

    private _realStatus as bool
    Status as bool:
        get:
            return _realStatus
    
    def constructor(pf as PollFunction):
        _pollFunc = pf
        _realStatus = _pollFunc()

    def Poll():
        oldStatus = _realStatus
        _realStatus = _pollFunc()
        if _realStatus != oldStatus:
            Changed(self)

    static def op_UnaryNegation(cond as Condition):
        nc = Condition({return not cond.Status})
        cond.Changed += nc.Poll
        return nc

    static def op_BitwiseAnd(condA as Condition, condB as Condition):
        nc = Condition({return condA.Status and condB.Status})
        condA.Changed += nc.Poll
        condB.Changed += nc.Poll
        return nc

    static def op_BitwiseOr(condA as Condition, condB as Condition):
        nc = Condition({return condA.Status or condB.Status})
        condA.Changed += nc.Poll
        condB.Changed += nc.Poll
        return nc

