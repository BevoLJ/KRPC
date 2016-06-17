import krpc
import time
import numpy as np
from scipy.constants import pi
from scipy.constants import g
from numba import jit


class Operations:

    conn = krpc.connect(name='name')
    KSC = conn.space_center
    vessel = KSC.active_vessel
    conn.krpcmj.apvessel = conn.space_center.active_vessel

    def __init__(self):
        super().__init__()

        self.mj = self.conn.krpcmj
        self.ap = self.vessel.auto_pilot
        self.control = self.vessel.control
        self.camera = self.KSC.camera
        self.CameraMode = self.KSC.CameraMode

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
        self.apoapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.apoapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.periapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')
        self.mean_anomaly = self.conn.add_stream(getattr, self.vessel.orbit, 'mean_anomaly')

        self.target_orbit = 1000000
        self.target_orbit_radius = self.target_orbit + self.radius_eq
        self.parking_orbit_alt = 250000
        self.parking_orbit_inc = 90

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

    def maneuver_burn_time(self, _maneuver_dv):
        _isp = max(self.specific_impulse(), 1)
        _thrust = max(1, self.max_thrust() * 1000)
        _mass = self.mass() * 1000

        return self.burn_time_calc(_isp, _thrust, _mass, _maneuver_dv)

    def ullage_rcs(self):
        _eng = self.get_active_engine()
        self.eng_action(_eng, "Shutdown Engine")
        time.sleep(1.25)
        self.control.throttle = 1
        while self.eng_status(_eng, "Propellant") != "Very Stable": time.sleep(.1)
        self.eng_action(_eng, "Activate Engine")

    def get_active_engine(self):
        for _eng in self.engines:
            if _eng.engine.active: return _eng

    def circ_dv(self):
        _circ_v = self.circular_speed_calc(self.apoapsis_radius(), self.mu)
        _v_ap = self.ap_v_calc(self.apoapsis_radius(), self.periapsis_radius(), self.mu)

        return self.circ_dv_calc(_circ_v, _v_ap)

    @staticmethod
    def eng_status(_eng, _status):
        _mod = _eng.modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF": return _m.get_field(_status)

    @staticmethod
    def eng_status_specific(_eng):
        _mod = _eng.modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF":
                return _m.get_field("Status")

    @staticmethod
    def eng_action(_eng, _action):
        _mod = _eng.modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF": _m.set_action(_action, True)

    @staticmethod
    @jit(nopython=True)
    def dv(_isp, _mass_full, _fuel_mass):
        return _isp * g * np.log(_mass_full / (_mass_full - _fuel_mass))

    @staticmethod
    @jit(nopython=True)
    def circular_speed_calc(_R_ap, _mu):
        return np.sqrt(_mu / _R_ap)

    @staticmethod
    @jit(nopython=True)
    def burn_time_calc(_isp, _thrust, _mass, _dv):
        _mdot = _thrust / g / _isp
        return _mass * (1 - np.e ** (-_dv / _isp / g)) / _mdot

    @staticmethod
    @jit(nopython=True)
    def time_to_burn(_node_eta, _burn_time):
        return _node_eta - (_burn_time / 2)

    @staticmethod
    @jit(nopython=True)
    def circ_dv_calc(_circ_v, _v_ap):
        return _circ_v - _v_ap

    @staticmethod
    @jit(nopython=True)
    def ap_dv_calc(_R_eq, _R_pe, _mu, _to, _v_ap):
        _t_radius = _to + _R_eq
        _t_ap_v = np.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
        return _v_ap - _t_ap_v

    @staticmethod
    @jit(nopython=True)
    def orbital_period(a, _mu):
        return 2 * pi * np.sqrt(a * a * a / _mu)

    @staticmethod
    @jit(nopython=True)
    def twr_calc(_thrust, _mass, _alt, _r_eq, _mu):
        return _thrust / ((_mu / ((_alt + _r_eq) ** 2)) * _mass)

    @staticmethod
    @jit(nopython=True)
    def ap_v_calc(_R_ap, _R_pe, _mu):
        return np.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
