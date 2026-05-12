from dataclasses import dataclass

@dataclass
class Aircraft:
    name: str
    type: str
    
    capacity: int
    weight_limit: int
    fuel_capacity: int