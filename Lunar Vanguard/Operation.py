import numpy
from Engine_Manager import EngineManager
from numba import jit


class Operations(EngineManager):

    def __init__(self):
        super().__init__()

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #           V E L O C I T Y              #
        #         A n d   D e l t a  V           #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def twr(self):
        _thrust = self.thrust()
        _mass = self.mass()
        _alt = self.altitude()
        _µ = self.gravitational_parameter

        _twr = (_thrust / ((_µ / ((_alt + self.radius_eq) ** 2)) * _mass))
        return _twr

    def stage_dv(self):
        _engine = self.get_active_engine()
        _isp = max(_engine.engine.specific_impulse, 1)
        # if _isp == 1:
        #     _isp = self.next_stage_isp()
        #     _engine = self._example_(self.current_stage_engs())
        _prop_used = _engine.engine.propellants
        _stage = _engine.decouple_stage
        _parts = self.vessel.parts.in_decouple_stage(_stage)
        _total_fuel_mass = 0
        _mass = self.mass()
        for _p in _parts:
            if _p.resources.names == _prop_used:
                _dry_mass = _p.dry_mass
                _wet_mass = _p.mass
                _total_fuel_mass = _total_fuel_mass + (_wet_mass - _dry_mass)

        @jit(nopython=True)
        def dv_calcs():
            _ve = _isp * 9.8
            _dv = _ve * numpy.log(_mass / (_mass - _total_fuel_mass))
            return _dv

        return dv_calcs()

    def apoapsis_speed(self):
        _R_ap = self.apoapsis_radius()
        _R_pe = self.periapsis_radius()
        _µ = self.gravitational_parameter

        @jit(nopython=True)
        def ap_dv_calc():
            _v_ap = numpy.sqrt((2 * _µ * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
            return _v_ap

        return ap_dv_calc()

    def target_apoapsis_speed_dv(self):
        _R_pe = self.periapsis_radius()
        _R_eq = self.radius_eq
        _µ = self.gravitational_parameter
        _to = float(self.target_orbit_alt)
        _v_ap = self.apoapsis_speed()

        @jit(nopython=True)
        def ap_dv_calc():
            _t_radius = _to + _R_eq
            _t_ap_v = numpy.sqrt((2 * _µ * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
            _t_ap_dv = _v_ap - _t_ap_v
            return _t_ap_dv

        return ap_dv_calc()

    def circular_speed(self):
        _R_ap = self.apoapsis_radius()
        _µ = self.gravitational_parameter

        @jit(nopython=True)
        def circular_speed_calc():
            _circ_v = numpy.sqrt(_µ / _R_ap)
            return _circ_v

        return circular_speed_calc()

    def circ_dv(self):
        _circ_v = self.circular_speed()
        _v_ap = self.apoapsis_speed()

        @jit(nopython=True)
        def circ_dv_calc():
            _circ_dv_calc = _circ_v - _v_ap
            return _circ_dv_calc

        return circ_dv_calc()

    def maneuver_burn_time(self, _maneuver_dv):
        _isp = max(self.specific_impulse(), 1)
        _thrust = max(1, self.max_thrust() * 1000)
        # if _isp == 1:
        #     _isp = self.next_stage_isp()
        #     _thrust = self.next_stage_thrust()
        _mass = self.mass() * 1000
        _dv = _maneuver_dv

        @jit(nopython=True)
        def burn_time_calc():
            _mdot = _thrust / 9.82 / _isp
            _burn_time = _mass * (1 - numpy.e ** (-_dv / _isp / 9.82)) / _mdot
            return _burn_time

        return burn_time_calc()

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_node_eta, _burn_time):
        return _node_eta - (_burn_time / 2)
