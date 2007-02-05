from solidfuel.Logic.Event import Event

class Timeline:
    def __init__(self):
        self._upcomingActions = []
        self._currentActions = []
        self._pastActions = []
        self._lastUpdate = 0.0
        self._everUpdated = False
        
        self.started = Event()
        self.finished = Event()
        self.updated = Event()

    def addAction(self, action):
        if action.end() and action.end() <= self._lastUpdate:
            self._pastActions.append(action)
        elif action.start() <= self._lastUpdate:
            self._currentActions.append(action)
        else:
            self._upcomingActions.append(action)

    def removeAction(self, action):
        for L in (self._pastActions, self._currentActions, self._upcomingActions):
            if action in L:
                L.remove(action)
                return

    def update(self, time, force=False):
        if not self._everUpdated:
            self.started.trigger()
            self._everUpdated = True
            
        for action in self._currentActions:
            if action.end() and action.end() <= time:
                self._currentActions.remove(action)
                self._pastActions.append(action)
                action.finished.trigger()
                if len(self._currentActions) == len(self._upcomingActions) == 0:
                    self.finished.trigger()
                if action.end():
                    action.update(action.end())
            else:
                action.update(time)
        if time == self._lastUpdate and not force:
            return
        elif time < self._lastUpdate:
            for action in self._pastActions + self._currentActions:
                if action.start() > time:
                    self._pastActions.remove(action)
                    self._upcomingActions.append(action)
                elif action.start() == time or (action.end() and action.end() > time):
                    self._pastActions.remove(action)
                    self._upcomingActions.append(action)
        else:
            for action in self._upcomingActions:
                if action.start() <= time:
                    action.update(action.start())
                    self._upcomingActions.remove(action)
                    self._currentActions.append(action)
                    action.started.trigger()
        self._lastUpdate = time
        self.updated.trigger()