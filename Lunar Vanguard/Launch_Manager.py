import numpy as np
from Operation import Operations
from numba import jit


class LaunchManager(Operations):

    def __init__(self):
        super().__init__()

        self.ap = self.vessel.auto_pilot
        self.control = self.vessel.control

        self.Q = self.conn.add_stream(getattr, self.vessel.flight(), 'dynamic_pressure')
        self.vessel_flight_bdy = self.conn.add_stream(self.vessel.flight, self.bdy_reference_frame())
        self.vessel_sur_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy(), 'speed')
        self.latitude = self.conn.add_stream(getattr, self.vessel.flight(), 'latitude')
        self.longitude = self.conn.add_stream(getattr, self.vessel.flight(), 'longitude')
        self.apoapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis_altitude = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.apoapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis')
        self.periapsis_radius = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis')

        self.lAz_data = self.azimuth_init()

        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #         S E T   H E A D I N G          #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    def pitch_and_heading(self):

        if self.vessel_sur_speed() < 80:
            self.ap.target_pitch_and_heading(90, 90)
        elif self.vessel_sur_speed() < 2200 or (self.apoapsis_altitude() < (self.target_orbit_alt * .92)):
            self.ap.target_pitch_and_heading(self.gravity_pitch(), self.azimuth(self.lAz_data))
        else:
            self.ap.target_pitch_and_heading(self.insertion_pitch() / 3.5, self.azimuth(self.lAz_data))

    def gravity_pitch(self):
        _t_ap_dv = self.target_apoapsis_speed_dv()
        _speed = self.vessel_sur_speed()

        @jit(nopython=True)
        def pitch_calcs():
            _pitch = (85 - (1.20 * np.sqrt(_speed))) + (_t_ap_dv / 6)
            return _pitch
        return pitch_calcs()

    def insertion_pitch(self):
        _circ_dv = self.circ_dv()
        _t_ap_dv = self.target_apoapsis_speed_dv()

        @jit(nopython=True)
        def pitch_calcs():
            if _circ_dv > 2000:
                return _t_ap_dv / 3
            elif _circ_dv > 1000:
                return _t_ap_dv / 2
            else:
                if _t_ap_dv >= 0:
                    return min(_t_ap_dv / 6, 10)
                else:
                    return max(_t_ap_dv / 6, -10)

        return pitch_calcs()

    def azimuth_init(self):

        _R_eq = self.radius_eq
        _inc = float(self.target_orbit_inc)
        _lat = self.latitude()
        _to = float(self.target_orbit_alt)
        _mu = self.mu
        _Rot_p = self.rotational_period
        node = "Ascending"

        if _inc < 0:
            node = "Descending"
            _inc = np.fabs(_inc)

        if (np.fabs(_lat)) > _inc:
            _inc = np.fabs(_lat)
        if (180 - np.fabs(_lat)) < _inc:
            _inc = (180 - np.fabs(_lat))

        velocity_eq = (2 * np.pi * _R_eq) / _Rot_p
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

            return np.rad2deg(np.fmod(np.arctan2(_VXRot, _VYRot) + 360, 360))
        _az = _az_calc()

        if _lAz_data[4] == "Ascending":
            return _az

        if _lAz_data[4] == "Descending":
            if _az <= 90:
                return 180 - _az
            elif _az >= 270:
                return 540 - _az

    def circ_dv(self):
        _circ_v = self.circular_speed_calc(self.apoapsis_radius(), self.mu)
        _v_ap = self.ap_v_calc(self.apoapsis_radius(), self.periapsis_radius(), self.mu)

        return self.circ_dv_calc(_circ_v, _v_ap)

    def target_apoapsis_speed_dv(self):
        _v_ap = self.ap_v_calc(self.apoapsis_radius(), self.periapsis_radius(), self.mu)

        return self.ap_dv_calc(self.radius_eq, self.periapsis_radius(), self.mu, float(self.target_orbit_alt), _v_ap)

    @staticmethod
    @jit(nopython=True)
    def twr_calc(_thrust, _mass, _alt, _r_eq, _mu):

        _twr = (_thrust / ((_mu / ((_alt + _r_eq) ** 2)) * _mass))
        return _twr

    @staticmethod
    @jit(nopython=True)
    def circ_dv_calc(_circ_v, _v_ap):
        _circ_dv_calc = _circ_v - _v_ap
        return _circ_dv_calc

    @staticmethod
    @jit(nopython=True)
    def ap_v_calc(_R_ap, _R_pe, _mu):
        _v_ap = np.sqrt((2 * _mu * _R_pe) / (_R_ap * (_R_ap + _R_pe)))
        return _v_ap

    @staticmethod
    @jit(nopython=True)
    def ap_dv_calc(_R_eq, _R_pe, _mu, _to, _v_ap):
        _t_radius = _to + _R_eq
        _t_ap_v = np.sqrt((2 * _mu * _R_pe) / (_t_radius * (_t_radius + _R_pe)))
        _t_ap_dv = _v_ap - _t_ap_v
        return _t_ap_dv

    def eng_status(self):
        _mod = self.get_active_engine().modules
        for _m in _mod:
            if _m.name == "ModuleEnginesRF":
                return _m.get_field("Status")
