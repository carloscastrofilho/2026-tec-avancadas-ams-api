class Estado:
    
    def __init__(self, id: int = None, estado: str = "", uf: str = ""):
        self.id = id
        self.estado = estado
        self.uf = uf

    def to_dict(self):
        return {
            "id": self.id,
            "estado": self.estado,
            "uf": self.uf
        }

    @staticmethod
    def from_dict(data: dict):
        return Estado(
            id=data.get("id"),
            estado=data.get("estado"),
            uf=data.get("uf")
        )
