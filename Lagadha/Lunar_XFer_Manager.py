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

    def xfer(self):
        time.sleep(8)
        self.control.activate_next_stage()
        time.sleep(2)
        self.mode = "Injection"
        print(self.mode)

    # noinspection PyAttributeOutsideInit
    def flameout(self, _mode):
        if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
            self.stage()
            self.mode = _mode

    # noinspection PyAttributeOutsideInit
    def named_flameout(self, _eng_name):
        for eng in self.engines:
            if eng.name == _eng_name:
                if self.eng_status_specific(eng) == "Flame-Out!":
                    return True
                else:
                    return False

    def injection_ETA(self):
        _eta = self.ut() + self.seconds_finder(6, 12, 0)
        return self.xfer_ETA(_eta, self.moon_LAN(), self.moon_argument_of_periapsis())

    def xfer_setup(self):
        self.control.rcs = True
        self.control.sas = True
        self.ap.sas_mode = self.KSC.SASMode.prograde
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.control.throttle = 0
        time.sleep(2)

    def warp_moon(self):
        while self.body().name == "Earth":
            if self.altitude() < 2000000:
                self.KSC.rails_warp_factor = 2
            elif self.altitude() < 35000000:
                self.KSC.rails_warp_factor = 3
            elif self.altitude() < 300000000:
                self.KSC.rails_warp_factor = 5
            elif self.altitude() < 375000000:
                self.KSC.rails_warp_factor = 4
            time.sleep(.01)
        self.KSC.rails_warp_factor = 0

    def capture_burn(self):
        self.KSC.warp_to(self.ut() + self.ETA_pe() - 90)
        self.ap.sas_mode = self.KSC.SASMode.retrograde
        time.sleep(40)
        self.ullage_rcs()
        self.control.throttle = 1
        while self.eccentricity() > .75: time.sleep(.1)