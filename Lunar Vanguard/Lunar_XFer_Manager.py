# import numpy as np
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

    def moon_future_mean(self, _t1):
        m_n = self.mean_motion(self.mu, self.moon_radius())
        m_delta = self.mean_delta_time(m_n, self.ut(), _t1)
        return self.moon_mean_anomaly() + m_delta
