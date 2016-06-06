# from Lunar_XFer_Manager import LunarXFerManager
from Launch_Manager import LaunchManager
# from numba import jit
# import time
import numpy as np


class Testing(LaunchManager):

    def __init__(self):
        super().__init__()

        self.ap = self.vessel.auto_pilot
        self.semi_major_axis = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')

        # self.moon_info()

        self.test()

    def test(self):
        print(self.stage_dv())
        print(" ")

        # while True:
        #     # print(_ecc)
        #     time.sleep(1)

    def moon_info(self):

        self.ap.engage()
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.ap.engage()

        print(" ")
        print("UT:                " + str(round(self.ut(), 2)))
        print("Earth_radius:      " + str(self.radius_eq / 1000))
        print(" ")
        print(" ")
        print("____V E S S E L_____")
        print(" ")
        print("  P R I M A R Y   O R B I T A L   E L E M E N T S ")
        print(" ")
        print("eccentricity:      " + str(round(self.eccentricity(), 2)))
        print("inclination:       " + str(round(np.rad2deg(self.inclination()), 2)))
        print("LAN:               " + str(round(self.LAN(), 2)))
        print("SMA:               " + str(round(self.semi_major_axis(), 2)))
        print("arg_of_pe:         " + str(round(self.argument_of_periapsis(), 2)))
        print("ETA_pe:            " + str(round(self.ETA_pe(), 2)))
        print(" ")
        print("  S E C O N D A R Y   O R B I T A L   E L E M E N T S ")
        print(" ")
        print("period:            " + str(round(self.period(), 2)))
        print("long of pe:        " + str(round(self.vessel_longitude_of_pe, 2)))
        print("mean_anomaly:      " + str(round(np.rad2deg(self.mean_anomaly()), 2)))
        print("ecc_anomaly:       " + str(round(np.rad2deg(self.eccentric_anomaly()), 2)))
        print("true_anomaly:      " + str(self.vessel_true_anomaly))
        print(" ")
        print("mean_an @ epoch:   " + str(round(np.rad2deg(self.moon_mean_anomaly_at_epoch()), 2)))
        print("moon_epoch:        " + str(self.moon_epoch()))
        print(" ")
        print("_______M O O N_______")
        print(" ")
        print("  P R I M A R Y   O R B I T A L   E L E M E N T S ")
        print(" ")
        print("eccentricity:      " + str(round(self.moon_eccentricity(), 2)))
        print("inclination:       " + str(round(np.rad2deg(self.moon_inclination()), 2)))
        print("LAN:               " + str(round(self.moon_LAN(), 2)))
        print("SMA:               " + str(round(self.moon_semi_major_axis(), 2)))
        print("arg_of_pe:         " + str(round(self.moon_argument_of_periapsis(), 2)))
        print("ETA_pe:            " + str(round(self.moon_ETA_pe(), 2)))
        print(" ")
        print("  S E C O N D A R Y   O R B I T A L   E L E M E N T S ")
        print(" ")
        print("period:            " + str(round(self.moon_period(), 2)))
        print("long of pe:        " + str(round(self.moon_longitude_of_pe, 2)))
        print("mean_anomaly:      " + str(round(np.rad2deg(self.moon_mean_anomaly()), 2)))
        print("ecc_anomaly:       " + str(round(np.rad2deg(self.moon_eccentric_anomaly()), 2)))
        print("true_anomaly:      " + str(self.moon_true_anomaly))
        print(" ")
        print("mean_an @ epoch:   " + str(round(np.rad2deg(self.moon_mean_anomaly_at_epoch()), 2)))
        print("moon_epoch:        " + str(self.moon_epoch()))

Testing()
