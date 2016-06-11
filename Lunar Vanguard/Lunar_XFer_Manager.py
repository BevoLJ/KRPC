import numpy as np
import time
# from numba import jit
from Orbit_Manager import OrbitManager


class LunarXFerManager(OrbitManager):
    def __init__(self):
        super().__init__()

        self.mode = "LEO"

        self.earth = self.KSC.bodies['Earth']
        self.moon = self.KSC.bodies['Moon'].orbit

        # M O O N   P R I M A R Y   O R B I T A L   E L E M E N T S

        self.moon_eccentricity = self.conn.add_stream(getattr, self.moon, 'eccentricity')
        self.moon_inclination = self.conn.add_stream(getattr, self.moon, 'inclination')
        self.moon_LAN = self.conn.add_stream(getattr, self.moon, 'longitude_of_ascending_node')
        self.moon_semi_major_axis = self.conn.add_stream(getattr, self.moon, 'semi_major_axis')
        self.moon_argument_of_periapsis = self.conn.add_stream(getattr, self.moon, 'argument_of_periapsis')
        self.moon_ETA_pe = self.conn.add_stream(getattr, self.moon, 'time_to_periapsis')

        # S E C O N D A R Y   O R B I T A L   E L E M E N T S

        self.moon_ETA_ap = self.conn.add_stream(getattr, self.moon, 'time_to_apoapsis')
        self.moon_mean_anomaly = self.conn.add_stream(getattr, self.moon, 'mean_anomaly')
        self.moon_eccentric_anomaly = self.conn.add_stream(getattr, self.moon, 'eccentric_anomaly')
        self.moon_true_anomaly = self.true_anomaly(self.moon_eccentricity(), self.moon_eccentric_anomaly())
        self.moon_longitude_of_pe = self.longitude_of_pe(self.moon_LAN(), self.moon_argument_of_periapsis())
        self.moon_period = self.conn.add_stream(getattr, self.moon, 'period')
        self.moon_radius = self.conn.add_stream(getattr, self.moon, 'radius')

        self.moon_mean_anomaly_at_epoch = self.conn.add_stream(getattr, self.moon, 'mean_anomaly_at_epoch')
        self.moon_epoch = self.conn.add_stream(getattr, self.moon, 'epoch')

    def moon_future_mean(self, _ta):
        _m_n = self.mean_motion(self.mu, self.moon_radius())
        _m_delta = self.mean_delta_time(_m_n, self.ut(), _ta)
        return self.moon_mean_anomaly() + _m_delta

    def moon_xfer_angle(self, _ta, _target_LAN, _target_arg_pe):
        _fut_moon_mean = self.moon_future_mean(_ta)
        _ves_l_pe = self.longitude_of_pe(self.LAN(), self.argument_of_periapsis()) % (2 * np.pi)
        _moon_l_pe = self.longitude_of_pe(_target_LAN, _target_arg_pe)
        return self.xfer_radians(_fut_moon_mean, _ves_l_pe, _moon_l_pe)

    def xfer_ETA(self, _ta, _target_LAN, _target_arg_pe):
        ang_v = self.ang_V_circle(self.period())
        _xfer_radians = self.moon_xfer_angle(_ta, _target_LAN, _target_arg_pe)
        if self.mean_anomaly() < _xfer_radians: _rad_diff = (_xfer_radians - self.mean_anomaly()) % (2 * np.pi)
        else: _rad_diff = (_xfer_radians - self.mean_anomaly()) % (2 * np.pi)
        return _rad_diff / ang_v

    def fix_aoa(self, injection_ETA):
        while 160 > injection_ETA > 35:
            injection_ETA = self.xfer_ETA(self.ut() + self.seconds_finder(5, 16, 00),
                                               self.moon_LAN(), self.moon_argument_of_periapsis())
            if self.angle_of_attack(self.vessel_orbit_direction(), self.vessel_velocity_direction()) > 30:
                self.ap.engage()
                self.control.rcs = True
                time.sleep(2)
                self.control.rcs = False
                while self.angle_of_attack(self.vessel_orbit_direction(), self.vessel_velocity_direction()) > 20:
                    time.sleep(.1)
                self.control.rcs = True
            print(injection_ETA)
            time.sleep(.1)

    def xfer(self):
        time.sleep(8)
        self.control.activate_next_stage()
        time.sleep(2)
        self.mode = "Injection"
        print(self.mode)

    # noinspection PyAttributeOutsideInit
    def flameout(self, _mode):
        if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
            self.control.activate_next_stage()
            time.sleep(1.5)
            self.mode = _mode
