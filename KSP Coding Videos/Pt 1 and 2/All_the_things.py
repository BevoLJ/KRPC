import krpc
import math
from numba import jit

conn = krpc.connect(name='name')

KSC = conn.space_center
vessel = KSC.active_vessel
ap = vessel.auto_pilot
control = vessel.control
parts = vessel.parts
engines = parts.with_module("ModuleEnginesRF")

body = vessel.orbit.body
bdy_reference_frame = conn.add_stream(getattr, body, 'reference_frame')
vessel_flight_bdy = conn.add_stream(vessel.flight, bdy_reference_frame())
vessel_speed = conn.add_stream(getattr, vessel_flight_bdy(), 'speed')

ETA_ap = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')


def twr():
    _thrust = vessel.thrust
    _mu = vessel.orbit.body.gravitational_parameter
    _Radius_eq = vessel.orbit.body.equatorial_radius
    _mass = vessel.mass
    _alt = vessel.flight().mean_altitude

    _twr = (_thrust / ((_mu / ((_alt + _Radius_eq) ** 2)) * _mass))
    return _twr


@jit(nopython=True)
def pitch(_speed):
    _pitch = (90 - (1.4 * math.sqrt(_speed)))
    return _pitch


def eng_status(spin_solids):
    for en in engines:
        if en.engine.active and (en.name != spin_solids):
            mod = en.modules
            for m in mod:
                if m.name == "ModuleEnginesRF":
                    return m.get_field("Status")


def stage_deltav(_part):
    for en in engines:
        if en.name == _part:
            _prop_used = en.engine.propellants
            _stage = en.decouple_stage
            _parts = vessel.parts.in_decouple_stage(_stage)
            for _p in _parts:
                if _p.resources.names == _prop_used:
                    _dry_mass = _p.dry_mass
                    _wet_mass = _p.mass
                    _fuel_mass = _wet_mass - _dry_mass

                    _ve = en.engine.specific_impulse * 9.8
                    _delta_v = _ve * math.log(vessel.mass / (vessel.mass - _fuel_mass))
                    return _delta_v
