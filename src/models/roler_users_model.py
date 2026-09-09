class Roller:
    
    def __init__(self, id: int = None, roller: str = ""):
        self.id = id
        self.roller = roller
        

    def to_dict(self):
        return {
            "id": self.id,
            "roller": self.roller            
        }

    @staticmethod
    def from_dict(data: dict):
        return Roller(
            id=data.get("id"),
            roller=data.get("roller")                        
        )