import numpy as np
from scipy.constants import pi
import time
from Operation import Operations
from numba import jit


class LaunchManager(Operations):

    def __init__(self):
        super().__init__()

        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())
        self.vessel_sur_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        self.latitude = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')

        self.lAz_data = self.azimuth_init()
        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        self.pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')

        self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #         S E T   H E A D I N G          #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def pitch_and_heading(self):

        if self.vessel_sur_speed() < 80: self.ap.target_pitch_and_heading(90, 90)
        elif self.vessel_sur_speed() < 2200 or (self.apoapsis_altitude() < (self.parking_orbit_alt * .92)):
            self.ap.target_pitch_and_heading(self.gravity_pitch(), self.azimuth(self.lAz_data))
        else:
            self.ap.target_pitch_and_heading(self.insertion_pitch(), self.azimuth(self.lAz_data))

    def gravity_pitch(self):
        _t_ap_dv = self.target_apoapsis_speed_dv()
        _speed = self.vessel_sur_speed()
        _circ_dv = self.circ_dv()

        @jit(nopython=True)
        def pitch_calcs():
            _pitch = (90 - ((1 + (_circ_dv / 7400)) * np.sqrt(_speed))) + (_t_ap_dv / (2 - (_circ_dv / 7400)))
            return _pitch

        return pitch_calcs()

    def insertion_pitch(self):
        _circ_dv = self.circ_dv()
        _t_ap_dv = self.target_apoapsis_speed_dv()
        _m = np.rad2deg(self.mean_anomaly())
        _burn_time = self.maneuver_burn_time(self.circ_dv())

        @jit(nopython=True)
        def pitch_calcs_low():
                return (_t_ap_dv * (_circ_dv / 1000)) + (_m - (180 - (_burn_time / 12)))

        @jit(nopython=True)
        def pitch_calcs_high():
                return (_t_ap_dv * (_circ_dv / 1000)) + (_m - 180)

        if self.parking_orbit_alt <= 300000: return pitch_calcs_low()
        else: return pitch_calcs_high()

    def azimuth_init(self):

        _R_eq = self.radius_eq
        _inc = float(self.parking_orbit_inc)
        _lat = self.latitude()
        _to = float(self.parking_orbit_alt)
        _mu = self.mu
        _Rot_p = self.rotational_period
        node = "Ascending"

        if _inc < 0:
            node = "Descending"
            _inc = np.fabs(_inc)

        if (np.fabs(_lat)) > _inc: _inc = np.fabs(_lat)

        if (180 - np.fabs(_lat)) < _inc: _inc = (180 - np.fabs(_lat))

        velocity_eq = (2 * pi * _R_eq) / _Rot_p
        t_orb_v = np.sqrt(_mu / (_to + _R_eq))

        return _inc, _lat, velocity_eq, t_orb_v, node

    @staticmethod
    def azimuth(_lAz_data):
        _inc = _lAz_data[0]
        _lat = _lAz_data[1]
        velocity_eq = _lAz_data[2]

        @jit(nopython=True)
        def _az_calc():
            inert_az = np.arcsin(max(min(np.cos(np.deg2rad(_inc)) / np.cos(np.deg2rad(_lat)), 1), -1))
            _VXRot = _lAz_data[3] * np.sin(inert_az) - velocity_eq * np.cos(np.deg2rad(_lat))
            _VYRot = _lAz_data[3] * np.cos(inert_az)

            return np.rad2deg(np.fmod(np.arctan2(_VXRot, _VYRot) + (2 * pi), (2 * pi)))
        _az = _az_calc()

        if _lAz_data[4] == "Ascending": return _az

        if _lAz_data[4] == "Descending":
            if _az <= 90: return 180 - _az
            elif _az >= 270: return 540 - _az

    def target_apoapsis_speed_dv(self):
        _v_ap = self.ap_v_calc(self.apoapsis_radius(), self.periapsis_radius(), self.mu)

        return self.ap_dv_calc(self.radius_eq, self.periapsis_radius(), self.mu, float(self.parking_orbit_alt), _v_ap)

    # noinspection PyAttributeOutsideInit
    def flameout(self, _mode):
        if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
            self.control.activate_next_stage()
            time.sleep(1.5)
            self.mode = _mode

    # noinspection PyAttributeOutsideInit
    def named_flameout(self, _eng_name):
        for eng in self.engines:
            if eng.name == _eng_name:
                if self.eng_status_specific(eng) == "Flame-Out!":
                    return True
                else:
                    return False

    def named_engines_activation(self, _eng_name):
        for _eng in self.engines:
            if _eng.name == _eng_name:
                if not _eng.engine.active:
                    _eng.engine.active = True
