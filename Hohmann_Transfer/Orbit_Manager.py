import numpy as np
import time
from scipy.constants import pi
from Operation import Operations
from numba import jit


class OrbitManager(Operations):
    def __init__(self):
        super().__init__()

        # P R I M A R Y   O R B I T A L   E L E M E N T S

        self.eccentricity = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        self.inclination = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.semi_major_axis = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.argument_of_periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')
        self.ETA_pe = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')

        # S E C O N D A R Y   O R B I T A L   E L E M E N T S

        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.eccentric_anomaly = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentric_anomaly')
        self.speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
        self.vessel_true_anomaly = self.true_anomaly(self.eccentricity(), self.eccentric_anomaly())
        self.vessel_longitude_of_pe = self.longitude_of_pe(self.LAN(), self.argument_of_periapsis())

        self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')

        self.mean_anomaly_at_epoch = self.conn.add_stream(getattr, self.vessel.orbit, 'mean_anomaly_at_epoch')
        self.epoch = self.conn.add_stream(getattr, self.vessel.orbit, 'epoch')

        # V E S S E L   I N F O

        self.orb_reference_frame = self.conn.add_stream(getattr, self.vessel.orbit.body, 'orbital_reference_frame')
        self.vessel_orbit_direction = self.conn.add_stream(self.vessel.direction, self.orb_reference_frame())
        self.vessel_velocity_direction = self.conn.add_stream(self.vessel.velocity, self.orb_reference_frame())
        self.bdy__non_rot_reference_frame = self.conn.add_stream(getattr, self.body, 'non_rotating_reference_frame')
        self.vessel_flight_bdy_non_rot = self.conn.add_stream(self.vessel.flight, self.bdy__non_rot_reference_frame())
        self.vessel_orb_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy_non_rot(), 'speed')

    def fix_aoa(self, _time_to_burn, _burn_time):
        while 90 > _time_to_burn > 35:
            _time_to_burn = self.time_to_burn(self.ETA_pe(), _burn_time)
            if self.angle_of_attack(self.vessel_orbit_direction(), self.vessel_velocity_direction()) > 30:
                self.ap.engage()
                self.control.rcs = True
                time.sleep(2)
                self.control.rcs = False
                while self.angle_of_attack(self.vessel_orbit_direction(), self.vessel_velocity_direction()) > 20:
                    time.sleep(.1)
                self.control.rcs = True
            time.sleep(.1)

    @staticmethod
    @jit(nopython=True)
    def angle_of_attack(_d, _v):
        _dp = _d[0] * _v[0] + _d[1] * _v[1] + _d[2] * _v[2]
        _vmag = np.sqrt(_v[0] ** 2 + _v[1] ** 2 + _v[2] ** 2)
        if _dp == 0: _angle = 0
        else: _angle = abs(np.arccos(_dp / _vmag) * (180. / np.pi))
        return _angle

    @staticmethod
    @jit(nopython=True)
    def ecc_to_mean_anomaly(_ec, _E):
        return _E - (_ec * np.sin(_E))

    @staticmethod
    @jit(nopython=True)
    def true_anomaly(_ec, _E):
        fak = np.sqrt(1.0 - _ec * _ec)
        return np.arctan2(fak * np.sin(_E), np.cos(_E) - _ec) / (pi / 180.0)

    @staticmethod
    @jit(nopython=True)
    def longitude_of_pe(_LAN, _arg_pe):
        return _LAN + _arg_pe

    @staticmethod
    @jit(nopython=True)
    def rad_two_pi(a):
        a %= 2 * np.pi
        if a < 0: return a + 2 * np.pi
        else: return a

    @staticmethod
    @jit(nopython=True)
    def mean_motion(_mu, _orbit_radius):
        return np.sqrt(_mu / (_orbit_radius * _orbit_radius * _orbit_radius))

    @staticmethod
    @jit(nopython=True)
    def ang_V_circle(_Period):
        return (2 * np.pi) / _Period

    @staticmethod
    @jit(nopython=True)
    def mean_delta_time(_n, _ta, _tb):
        return _n * (_tb - _ta)

    @staticmethod
    @jit(nopython=True)
    def seconds_finder(_day, _hour, _mins):
        _d_h = (_day * 24) + _hour
        _h_m = (_d_h * 60) + _mins
        return _h_m * 60

    @staticmethod
    @jit(nopython=True)
    def xfer_radians(_fut_moon_mean, _ves_l_pe, _target_l_pe):
        _diff_l_pe = np.fabs(_target_l_pe - _ves_l_pe)
        return np.abs(_fut_moon_mean - _diff_l_pe - np.pi)

    @staticmethod
    @jit(nopython=True)
    def transfer_injection_dv(_mu, _sma, _to):
        _a_xfer = (_sma + _to) / 2
        v_xfer_init = np.sqrt(_mu * ((2 / _sma) - (1 / _a_xfer)))
        return v_xfer_init - np.sqrt(_mu / _sma)
