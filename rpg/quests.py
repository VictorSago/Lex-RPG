
class Quest:
    def __init__(self, description: str) -> None:
        self.description = description
        self._is_complete = False

    def complete(self) -> None:
        self._is_complete = True
    
    def is_comlete(self) -> bool:
        return self._is_complete
