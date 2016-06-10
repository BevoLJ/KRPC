from Lunar_XFer_Manager import LunarXFerManager
# from Launch_Manager import LaunchManager
# from scipy.constants import pi
import numpy as np
from numba import jit
# from numba import jit
# import time


class Testing(LunarXFerManager):

    def __init__(self):
        super().__init__()

        # self.ap = self.vessel.auto_pilot
        # self.semi_major_axis = self.conn.add_stream(getattr, self.vessel.orbit, 'semi_major_axis')
        # self.period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')

    @staticmethod
    def list_modules(_part):
        for p in _part:
            mod = p.modules
            for m in mod:
                print(m.name)

    def list_actions(self, _mod):
        mod = self.get_active_engine().modules
        print(" ")
        print("- A C T I O N S -")
        for m in mod:
            if m.name == _mod:
                print("- " + m.name)
                act = m.actions
                for a in act:
                    print("   " + a)
        print(" ")
        print("- F I E L D S -")
        for m in mod:
            if m.name == _mod:
                print("- " + m.name)
                flds = m.fields
                for k, v in flds.items():
                    print("   " + k, ": " + v)

    @staticmethod
    def list_parts(_parts):
        for p in _parts:
            print("-------")
            print(p)
            print(" Engine Name : " + p.name)
            print("  Activated Stage: " + str(p.stage))
            print("  Decouple Stage:  " + str(p.decouple_stage))

    # def mean_at_ut(self):
    #
    #     _o_period = self.moon.period
    #     _ecc = self.moon.eccentricity
    #     _ut = self.ut()
    #     _epoch = self.moon.epoch
    #     _epoch_mean = self.moon.mean_anomaly_at_epoch
    #
    #     @jit(nopython=True)
    #     def _calcs():
    #
    #         _motion = 2 * pi / _o_period
    #         _m_a_ut = (_epoch_mean + (_ut - _epoch)) * _motion
    #
    #         return _m_a_ut
    #
    #     if _ecc > 1:
    #         return self.rad_two_pi(_calcs())
    #     return _calcs()

    @staticmethod
    @jit(nopython=True)
    def rad_two_pi(a):
        a %= 2 * np.pi
        if a < 0: return a + 2 * np.pi
        else: return a

    def test(self):
        print(self.stage_dv())
        print(" ")

        # while True:
        #     # print(_ecc)
        #     time.sleep(1)

    # def moon_info(self):
    #
    #     self.ap.engage()
    #     self.ap.reference_frame = self.vessel.orbital_reference_frame
    #     self.ap.engage()
    #
    #     print(" ")
    #     print("UT:                " + str(round(self.ut(), 2)))
    #     print("Earth_radius:      " + str(self.radius_eq / 1000))
    #     print(" ")
    #     print(" ")
    #     print("____V E S S E L_____")
    #     print(" ")
    #     print("  P R I M A R Y   O R B I T A L   E L E M E N T S ")
    #     print(" ")
    #     print("eccentricity:      " + str(round(self.eccentricity(), 2)))
    #     print("inclination:       " + str(round(np.rad2deg(self.inclination()), 2)))
    #     print("LAN:               " + str(round(self.LAN(), 2)))
    #     print("SMA:               " + str(round(self.semi_major_axis(), 2)))
    #     print("arg_of_pe:         " + str(round(self.argument_of_periapsis(), 2)))
    #     print("ETA_pe:            " + str(round(self.ETA_pe(), 2)))
    #     print(" ")
    #     print("  S E C O N D A R Y   O R B I T A L   E L E M E N T S ")
    #     print(" ")
    #     print("period:            " + str(round(self.period(), 2)))
    #     print("long of pe:        " + str(round(self.vessel_longitude_of_pe, 2)))
    #     print("mean_anomaly:      " + str(round(np.rad2deg(self.mean_anomaly()), 2)))
    #     print("ecc_anomaly:       " + str(round(np.rad2deg(self.eccentric_anomaly()), 2)))
    #     print("true_anomaly:      " + str(self.vessel_true_anomaly))
    #     print(" ")
    #     print("mean_an @ epoch:   " + str(round(np.rad2deg(self.moon_mean_anomaly_at_epoch()), 2)))
    #     print("moon_epoch:        " + str(self.moon_epoch()))
    #     print(" ")
    #     print("_______M O O N_______")
    #     print(" ")
    #     print("  P R I M A R Y   O R B I T A L   E L E M E N T S ")
    #     print(" ")
    #     print("eccentricity:      " + str(round(self.moon_eccentricity(), 2)))
    #     print("inclination:       " + str(round(np.rad2deg(self.moon_inclination()), 2)))
    #     print("LAN:               " + str(round(self.moon_LAN(), 2)))
    #     print("SMA:               " + str(round(self.moon_semi_major_axis(), 2)))
    #     print("arg_of_pe:         " + str(round(self.moon_argument_of_periapsis(), 2)))
    #     print("ETA_pe:            " + str(round(self.moon_ETA_pe(), 2)))
    #     print(" ")
    #     print("  S E C O N D A R Y   O R B I T A L   E L E M E N T S ")
    #     print(" ")
    #     print("period:            " + str(round(self.moon_period(), 2)))
    #     print("long of pe:        " + str(round(self.moon_longitude_of_pe, 2)))
    #     print("mean_anomaly:      " + str(round(np.rad2deg(self.moon_mean_anomaly()), 2)))
    #     print("ecc_anomaly:       " + str(round(np.rad2deg(self.moon_eccentric_anomaly()), 2)))
    #     print("true_anomaly:      " + str(self.moon_true_anomaly))
    #     print(" ")
    #     print("mean_an @ epoch:   " + str(round(np.rad2deg(self.moon_mean_anomaly_at_epoch()), 2)))
    #     print("moon_epoch:        " + str(self.moon_epoch()))

Testing()
