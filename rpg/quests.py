
class Quest:
    # TODO: completion is a stored flag set by Game for now. Later: derive it
    # (subclasses overriding is_complete(), sub-quests as a list of Quests).
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self._is_complete = False

    def complete(self) -> None:
        self._is_complete = True
    
    def is_complete(self) -> bool:
        return self._is_complete
