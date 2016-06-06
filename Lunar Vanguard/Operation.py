import krpc
import numpy as np
from numba import jit


class Operations:

    conn = krpc.connect(name='name')
    KSC = conn.space_center
    vessel = KSC.active_vessel

    def __init__(self):
        super().__init__()

        self.target_orbit_alt = 0
        self.target_orbit_inc = 0

        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")

        self.body = self.vessel.orbit.body
        self.rotational_period = self.body.rotational_period
        self.mu = self.body.gravitational_parameter
        self.radius_eq = self.body.equatorial_radius
        self.bdy_reference_frame = self.conn.add_stream(getattr, self.body, 'reference_frame')

        self.parts = self.vessel.parts
        self.engines = self.parts.with_module("ModuleEnginesRF")

        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.max_thrust = self.conn.add_stream(getattr, self.vessel, 'max_thrust')
        self.specific_impulse = self.conn.add_stream(getattr, self.vessel, 'vacuum_specific_impulse')
        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #           V E L O C I T Y              #
        #         A n d   D e l t a  V           #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def stage_dv(self):
        _engine = self.get_active_engine()
        _isp = max(_engine.engine.specific_impulse, 1)
        _prop_used = _engine.engine.propellants
        _stage = _engine.decouple_stage
        _parts = self.vessel.parts.in_decouple_stage(_stage)
        _fuel_mass = 0

        for _p in _parts:
            if _p.resources.names == _prop_used:
                _dry_mass = _p.dry_mass
                _wet_mass = _p.mass
                _fuel_mass = _fuel_mass + (_wet_mass - _dry_mass)

        return self.dv(_isp, self.mass(), _fuel_mass)

    @staticmethod
    @jit(nopython=True)
    def dv(_isp, _mass_full, _fuel_mass):
        _dv = _isp * 9.8 * np.log(_mass_full / (_mass_full - _fuel_mass))
        return _dv

    @staticmethod
    @jit(nopython=True)
    def circular_speed_calc(_R_ap, _mu):
        _circ_v = np.sqrt(_mu / _R_ap)
        return _circ_v

    def maneuver_burn_time(self, _maneuver_dv):
        _isp = max(self.specific_impulse(), 1)
        _thrust = max(1, self.max_thrust() * 1000)
        _mass = self.mass() * 1000

        return self.burn_time_calc(_isp, _thrust, _mass, _maneuver_dv)

    @staticmethod
    @jit(nopython=True)
    def burn_time_calc(_isp, _thrust, _mass, _dv):
        _mdot = _thrust / 9.82 / _isp
        _burn_time = _mass * (1 - np.e ** (-_dv / _isp / 9.82)) / _mdot
        return _burn_time

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_node_eta, _burn_time):
        return _node_eta - (_burn_time / 2)

    def get_active_engine(self):
        for _eng in self.engines:
            if _eng.engine.active: return _eng
