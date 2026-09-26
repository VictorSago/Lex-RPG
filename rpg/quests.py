
class Quest:
    def __init__(self, description: str) -> None:
        self.description = description

    def complete(self) -> None:
        pass
    
    def is_comlete(self) -> bool:
        return False
