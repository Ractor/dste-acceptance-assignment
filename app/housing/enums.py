from enum import Enum

class OceanProximityEnum(str, Enum):
    LESS_THAN_1H_OCEAN = "<1H OCEAN"
    INLAND = "INLAND"
    ISLAND = "ISLAND"
    NEAR_BAY = "NEAR BAY"
    NEAR_OCEAN = "NEAR OCEAN"
    
