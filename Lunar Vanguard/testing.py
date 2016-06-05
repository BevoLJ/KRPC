from Launch_Manager import LaunchManager
# from numba import jit
import time
import numpy as np


class Testing(LaunchManager):

    def __init__(self):
        super().__init__()

        self.target_orbit_inc = 28
        self.lAz_data = self.azimuth_init()
        self.Earth = self.KSC.bodies['Earth']
        self.Moon = self.KSC.bodies['Moon']

        self.moon_info()

        # while True:
        #     print(_ecc)
        #     time.sleep(1)

    def test(self):
        # print(self.lAz_data)
        print("Test all things")
        print(self.azimuth_init2(self.lAz_data))

    def moon_info(self):

        # _ut = round(self.KSC.ut, 2)

        self.ap.engage()
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.ap.engage()

        print(" ")
        print("____V E S S E L_____")
        print(" ")
        print("SMA 250km Orbit:   " + (str((self.radius_eq / 1000) + 250)))
        print("longitude:         " + str(round(self.longitude(), 2)))
        print("latitude:          " + str(round(self.latitude(), 2)))
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

        while True:
            self.ap.target_direction = (0, 1, 0)
            print("orb_dir: " + str(self.vessel_orbit_direction()))
            print(self.vessel_orb_speed())
            time.sleep(1)

        # print(self.ap.target_direction)

Testing()
