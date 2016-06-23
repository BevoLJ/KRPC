import time
import numpy as np
from UI import UI
from Lunar_XFer_Manager import LunarXFerManager


class LaunchControl(UI):
    def __init__(self):
        super().__init__()

        # self.mode = "Testing"
        self.mode = "Launch Prep"
        self.camera.mode = self.CameraMode.free
        self.falafels = True

    def launch(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              L A U N C H               #
        #             P R O G R A M              #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        print("For 300km Parking Orbit - Moon Shot launch at LAN = 334.56846 - 6.68379")
        ui = UI()
        _tp = self.orbital_period(self.parking_orbit_alt + self.radius_eq, self.mu)

        while self.mode == "Launch Prep":
            # if self.control.get_action_group(9):
            #     self.control.throttle = 1
            #     self.control.activate_next_stage()
            #     time.sleep(1.5)
            #     self.control.activate_next_stage()
            #     self.mode = "Launch"
            self.control.throttle = 1
            self.control.activate_next_stage()
            self.mode = "Launch"
            time.sleep(1)

        while self.mode != "Orbit":
            self.pitch_and_heading()

            if self.mode == "Testing":
                self.list_parts(self.engines)
                self.mode = "Orbit"

            if self.falafels is True:
                if self.altitude() > 80000:
                    self.control.toggle_action_group(8)
                    self.falafels = False

            if self.mode == "Launch":
                _twr = self.twr_calc(self.thrust(), self.mass(), self.altitude(), self.radius_eq, self.mu)
                if _twr > 1:
                    self.lAz_data = self.azimuth_init()
                    self.control.activate_next_stage()
                    self.mode = "Booster"

            if self.mode == "Booster":
                self.flameout("Core Stage")

            if self.mode == "Core Stage":

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
                if (self.circ_dv() < 10) or (_tp < self.period()):
                    self.control.throttle = 0
                    self.mode = "Orbit"

            if self.circ_dv() > 500: time.sleep(.1)
            ui.gravity_turn(self.mode)

        ui.remove_ui()
        self.control.rcs = True
        self.control.activate_next_stage()
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

        self.control.rcs = True
        self.control.sas = True
        self.ap.sas_mode = self.KSC.SASMode.prograde
        self.control.throttle = 0
        time.sleep(1)
        self.ap.reference_frame = self.vessel.orbital_reference_frame
        print(self.mode)
        ui = UI()

        while self.mode != "Xfered":

            if self.mode == "Testing":
                # print(np.rad2deg(self.moon_mean_anomaly()))
                print(self.get_active_engine().name)
                self.mode = "Xfered"

            if self.mode == "LEO Cruise":
                self.injection_ETA = self.xfer_ETA(self.ut() + self.seconds_finder(5, 16, 00),
                                                   self.moon_LAN(), self.moon_argument_of_periapsis())
                self.KSC.warp_to(self.ut() + self.injection_ETA - 200)
                if self.injection_ETA < 120:
                    self.ullage_rcs()
                    self.mode = "Agena"
                    print(self.mode)
                    time.sleep(2)

            if self.mode == "Agena":
                if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!":
                    self.control.activate_next_stage()
                    self.mode = "Injection"
                    print(self.mode)
                    time.sleep(2)

            if self.mode == "Injection":
                if self.apoapsis_radius > 395000000: self.mode = "Transfer"

            time.sleep(.1)
            ui.transfer(self.mode)

        print("Done")


def main():
    # LaunchControl().launch()
    LunarTransfer().transfer()


main()
