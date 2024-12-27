from vector3 import OrthonormalBasis, Vector3
from abc import abstractmethod, ABC
from rtutils import pi, fmin, fmax
class PDF(ABC):
    @abstractmethod
    def Value(self: 'PDF', direction: Vector3) -> float:
        pass
    def Generate(self: 'PDF') -> Vector3:
        pass
class SpherePDF(PDF):
    def __init__(self: 'SpherePDF') -> 'SpherePDF':
        pass
    def Value(self: 'SpherePDF', direction: Vector3) -> float:
        return 1 / (4*pi)
    def Generate(self: 'SpherePDF') -> Vector3:
        return Vector3.RandomUnitVector()
class CosPDF(PDF):
    def __init__(self: 'CosPDF', w: Vector3) -> 'CosPDF':
        self.uwv = OrthonormalBasis(w)
    def Value(self: 'CosPDF', direction: Vector3) -> float:
        cosTheta = direction.UnitVector().dot(self.uwv.w())
        return fmax(0, cosTheta/pi)
    def Generate(self: 'CosPDF') -> Vector3:
        return self.uvw.Transform(Vector3.RandomCosineDirection())
    