class Timeline:
    def __init__(self):
        self._upcomingActions = []
        self._currentActions = []
        self._pastActions = []
        self._lastUpdate = 0.0
        self.updated = Event()

    def addAction(self, action):
        if action.end() <= self._lastUpdate:
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

    def update(self, time):
        for action in self._upcomingActions:
            if action.start() <= time:
                self._upcomingActions.remove(action)
                self._currentActions.append(action)
        for action in self._currentActions:
            action.update(time)
            if action.end() <= time:
                self._currentActions.remove(action)
                self._pastActions.append(action)
        self._lastUpdate = time
        self.updated.trigger()
            
            
