import numpy as np
from Operation import Operations
from numba import jit


class OrbitManager(Operations):
    def __init__(self):
        super().__init__()

        self.Earth = self.KSC.bodies['Earth']
        self.Moon = self.KSC.bodies['Moon']

        # P R I M A R Y   O R B I T A L   E L E M E N T S

        self.eccentricity = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
        self.inclination = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        self.LAN = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
        self.semi_major_axis = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.argument_of_periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'argument_of_periapsis')
        self.ETA_pe = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')

        # S E C O N D A R Y   O R B I T A L   E L E M E N T S

        self.ETA_ap = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
        self.mean_anomaly = self.conn.add_stream(getattr, self.vessel.orbit, 'mean_anomaly')
        self.eccentric_anomaly = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentric_anomaly')
        self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')
        self.speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
        self.true_anomaly = self.true_anomaly(self.eccentricity, self.eccentric_anomaly)

        # V E S S E L   I N F O

        self.orb_reference_frame = self.conn.add_stream(getattr, self.vessel, 'orbital_reference_frame')
        self.vessel_orbit_direction = self.conn.add_stream(self.vessel.direction, self.orb_reference_frame())
        self.bdy__non_rot_reference_frame = self.conn.add_stream(getattr, self.body, 'non_rotating_reference_frame')
        self.vessel_flight_bdy_non_rot = self.conn.add_stream(self.vessel.flight, self.bdy__non_rot_reference_frame())
        self.vessel_orb_speed = self.conn.add_stream(getattr, self.vessel_flight_bdy_non_rot(), 'speed')

    @staticmethod
    @jit(nopython=True)
    def true_anomaly(_ec, _E):
        fak = np.sqrt(1.0 - _ec * _ec)
        phi = np.arctan2(fak * np.sin(_E), np.cos(_E) - _ec) / (np.pi / 180.0)

        return np.round(phi, 2)

    @staticmethod
    @jit(nopython=True)
    def longitude_of_pe(_LAN, _arg_pe):
        _long_pe = _LAN + _arg_pe
        return _long_pe
