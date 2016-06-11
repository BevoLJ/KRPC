import time
import numpy as np
from Launch_UI import LaunchUI
from Lunar_XFer_Manager import LunarXFerManager


class LaunchControl(LaunchUI):
    def __init__(self):
        super().__init__()

        self.mode = "Launch Prep"
        self.camera.mode = self.CameraMode.free

    def launch(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              L A U N C H               #
        #             P R O G R A M              #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        print("For 400km Parking Orbit - Moon Shot launch at LAN = 334.56846 - 6.68379")
        ui = LaunchUI()

        while self.mode == "Launch Prep":
            if self.control.get_action_group(9): self.mode = "Launch"; self.control.activate_next_stage()
            time.sleep(1)

        while self.mode != "Orbit":
            self.pitch_and_heading()

            if self.mode == "Launch":
                self.control.throttle = 1
                _twr = self.twr_calc(self.thrust(), self.mass(), self.altitude(), self.radius_eq, self.mu)
                if _twr > 1:
                    self.lAz_data = self.azimuth_init()
                    self.control.activate_next_stage()
                    self.mode = "Booster Stage"

            if self.mode == "Booster Stage": self.flameout("Mid Stage")

            if self.mode == "Mid Stage": self.flameout("Upper Stage")

            if self.mode == "Upper Stage":
                if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
                    self.control.throttle = 0
                    time.sleep(1.5)
                    self.control.activate_next_stage()
                    self.control.rcs = True
                    self.mode = "Cruise"

            if self.mode == "Cruise":
                if self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 5:
                    self.ullage_rcs()
                    self.mode = "Orbit Insertion"

            if self.mode == "Orbit Insertion":
                self.control.rcs = False
                if (self.circ_dv() < 10) or (self.orbital_period(self.target_orbit_alt + self.radius_eq,
                                                                 self.mu) < self.period()):
                    self.control.throttle = 0
                    self.mode = "Orbit"

            if self.circ_dv() > 500: time.sleep(.1)

            ui.gravity_turn(self.mode)

        self.control.rcs = True
        self.ap.disengage()
        self.control.sas = True
        time.sleep(2)


class LunarTransfer(LunarXFerManager):
    def __init__(self):
        super().__init__()

        self.mode = "LEO Cruise"
        # self.mode = "Testing"
        self.injection_ETA = 0
        self.camera.mode = self.CameraMode.free

    def transfer(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #               L U N A R                #
        #            T R A N S F E R             #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.control.rcs = False
        self.control.throttle = 0
        time.sleep(1)
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        self.ap.target_direction = (0, 1, 0)
        self.ap.engage()
        print(self.mode)

        while self.mode != "Xfered":
            self.injection_ETA = self.xfer_ETA(self.ut() + self.seconds_finder(5, 16, 00),
                                               self.moon_LAN(), self.moon_argument_of_periapsis())

            if self.mode == "Testing":
                print(np.rad2deg(self.moon_mean_anomaly()))
                self.mode = "Xfered"

            if self.mode == "LEO Cruise":
                self.KSC.warp_to(self.ut() + self.injection_ETA - 140)
                if self.injection_ETA < 130: self.mode = "AoA"; print(self.mode); time.sleep(2)

            if self.mode == "AoA":
                print(self.injection_ETA)
                if self.injection_ETA > 170: self.mode = "LEO Cruise"
                if self.injection_ETA > 25: self.fix_aoa(self.injection_ETA)
                elif self.injection_ETA <= 25: self.xfer()

            if self.mode == "Injection":
                self.flameout("Transfer")
                if self.vessel.mass < 20: self.mode = "Xfered"; print(self.mode)

            time.sleep(.1)

        print("Done")


def main():
    LaunchControl().launch()
    LunarTransfer().transfer()


main()
