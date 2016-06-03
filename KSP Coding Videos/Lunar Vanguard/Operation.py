import krpc
import math
from numba import jit


class Operations:

    conn = krpc.connect(name='name')

    KSC = conn.space_center
    vessel = KSC.active_vessel
    ap = vessel.auto_pilot
    control = vessel.control
    parts = vessel.parts
    engines = parts.with_module("ModuleEnginesRF")

    def __init__(self):

        self.target_orbit = 0

        self.body = self.vessel.orbit.body
        self.radius_eq = self.vessel.orbit.body.equatorial_radius

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.apoapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.periapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.apoapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        # vessel_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
        # heading = conn.add_stream(getattr, vessel.flight(), 'heading')

        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body, 'reference_frame')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())
        self.vessel_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        # altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

        self.spin_solids = "SnubOtron"

    def print_to(self):
        print(self.target_orbit)

    def twr(self):
        _thrust = self.vessel.thrust
        _mass = self.vessel.mass
        _alt = self.vessel.flight().mean_altitude
        _mu = self.vessel.orbit.body.gravitational_parameter

        _twr = (_thrust / ((_mu / ((_alt + self.radius_eq) ** 2)) * _mass))
        return _twr

    def apoapsis_v_dv(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _t_radius = self.target_orbit + self.vessel.orbit.radius
        _mu = self.vessel.orbit.body.gravitational_parameter

        @jit(nopython=True)
        def ap_dv_calc():
            _v_ap = math.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            _t_ap_v = math.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _t_ap_v - _v_ap
            return _t_ap_dv

        return ap_dv_calc()

    def pitch(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _speed = self.vessel_speed()
        _mu = self.vessel.orbit.body.gravitational_parameter
        _to = self.target_orbit

        @jit(nopython=True)
        def pitch_calcs():
            _t_radius = _to + _R_eq
            _v_ap = math.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            _t_ap_v = math.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _t_ap_v - _v_ap
            _p_ap_dv = _t_ap_dv / 4
            _pitch = (90 - (1.2 * math.sqrt(_speed))) - _p_ap_dv
            return _pitch

        return pitch_calcs()

    def eng_status(self):
        _mod = self.get_active_engine().modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF":
                return _m.get_field("Status")

    def get_active_engine_list(self):
        _active_engines_list = []
        for _eng in self.engines:
            if _eng.engine.active: _active_engines_list.append(_eng)
        return _active_engines_list

    def get_active_engine(self):
        for _eng in self.engines:
            if _eng.engine.active: return _eng

    def stage_deltav(self):
        _engine = self.get_active_engine()
        _prop_used = _engine.engine.propellants
        _stage = _engine.decouple_stage
        _parts = self.vessel.parts.in_decouple_stage(_stage)
        _total_fuel_mass = 0
        _isp = _engine.engine.specific_impulse
        _mass = self.vessel.mass
        for _p in _parts:
            if _p.resources.names == _prop_used:
                _dry_mass = _p.dry_mass
                _wet_mass = _p.mass
                _total_fuel_mass = _total_fuel_mass + (_wet_mass - _dry_mass)

        @jit(nopython=True)
        def dv_calcs():
            _ve = _isp * 9.8
            _delta_v = _ve * math.log(_mass / (_mass - _total_fuel_mass))
            return _delta_v

        return dv_calcs()

    def circ_dv(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _mu = self.vessel.orbit.body.gravitational_parameter

        @jit(nopython=True)
        def circ_dv_calc():
            _circ_v = math.sqrt(_mu / _R_ap)
            _v_ap = math.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            _circ_dv_calc = _circ_v - _v_ap
            return _circ_dv_calc

        return circ_dv_calc()

    def active_next_stage_engines(self):
        _stage = self.get_active_engine().decouple_stage
        for _eng in self.engines:
            if _eng.decouple_stage == (_stage - 1): _eng.engine.active = True

    def maneuver_burn_time(self, _maneuver_deltav):
        _isp = self.vessel.vacuum_specific_impulse
        _mass = self.vessel.mass * 1000
        _dv = _maneuver_deltav
        _thrust = self.vessel.max_thrust * 1000

        @jit(nopython=True)
        def burn_time_calc():
            _burn_time = 9.82 * _mass * _isp * (1 - math.e ** (-_dv / (9.82 * _isp))) / _thrust
            return _burn_time

        return burn_time_calc()

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_ut, _node_eta, _burn_time):
        return _ut - _node_eta - (_burn_time / 2)
