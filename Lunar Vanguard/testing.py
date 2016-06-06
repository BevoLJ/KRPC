# from Orbit_Manager import OrbitManager
from Launch_Manager import LaunchManager
# from numba import jit
# import time
import numpy as np


class Testing(LaunchManager):

    def __init__(self):
        super().__init__()

        self.ap = self.vessel.auto_pilot

        self.test()

    def test(self):
        print(" ")
        print("  stage_dv:            " + str(round(self.stage_dv(), 2)))
        print(" ")

        # while True:
        #     print(_ecc)
        #     time.sleep(1)

    def moon_info(self):

        self.ap.engage()
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.ap.engage()

        print(" ")
        print("____V E S S E L_____")
        print(" ")
        print("SMA 250km Orbit:   " + (str((self.radius_eq / 1000) + 250)))
        print("mean_altitude:     " + str(round(self.altitude(), 2) / 1000))
        print(" ")
        print("______E A R T H_____")
        print(" ")
        print("UT:                " + str(round(self.ut(), 2)))
        print("Earth_radius:      " + str(self.radius_eq / 1000))
        print("rotational_period: " + str(self.rotational_period))
        print("mean_anomaly:      " + str(np.rad2deg(self.Earth.orbit.mean_anomaly)))
        print("eccentric_anomaly: " + str(np.rad2deg(self.Earth.orbit.eccentric_anomaly)))
        print(" ")
        print("_______M O O N_______")
        print(" ")
        print("SMA:               " + str(round(self.Moon.orbit.semi_minor_axis, 2)))
        print("period:            " + str(round(self.Moon.orbit.period, 2)))
        print("eccentricity:      " + str(round(self.Moon.orbit.eccentricity, 2)))
        print("inclination:       " + str(round(np.rad2deg(self.Moon.orbit.inclination), 2)))
        print("LAN:               " + str(round(np.rad2deg(self.Moon.orbit.longitude_of_ascending_node), 2)))
        print("mean_anomaly:      " + str(round(np.rad2deg(self.Moon.orbit.mean_anomaly), 2)))
        phi = self.true_anomaly(self.Moon.orbit.eccentricity, self.Moon.orbit.eccentric_anomaly)
        print("Moon true_anomaly: " + str(phi))

Testing()
