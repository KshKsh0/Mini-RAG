from enum import Enum

class VectorDBEnums(Enum):
    QDRANT= 'QDRANT'

class DistanceFunction(Enum):
    COSINE = 'Cosine'
    DOT ='Dot'