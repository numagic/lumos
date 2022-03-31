from lumos.models.composition import ModelMaker
from lumos.models.simple_vehicle_on_track import SimpleVehicleOnTrack
from lumos.models.tires.pacejka import MF52
from lumos.models.tires.perantoni import PerantoniTire
from lumos.models.vehicles.simple_vehicle import SimpleVehicle
from lumos.models.kinematics import TrackPosition2D
from lumos.models.aero.aero import ConstAero, GPAero, MLPAero

ModelMaker.add_to_registry(MF52)
ModelMaker.add_to_registry(PerantoniTire)

ModelMaker.add_to_registry(SimpleVehicle)
ModelMaker.add_to_registry(TrackPosition2D)
ModelMaker.add_to_registry(SimpleVehicleOnTrack)

ModelMaker.add_to_registry(ConstAero)
ModelMaker.add_to_registry(GPAero)
ModelMaker.add_to_registry(MLPAero)
