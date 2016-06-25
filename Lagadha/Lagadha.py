import time
from UI import UI
from Lunar_XFer_Manager import LunarXFerManager
import numpy as np


class LaunchControl(UI):
    def __init__(self):
        super().__init__()

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
        _tp = self.orbital_period(self.parking_orbit_alt + self.radius_eq, self.mu)
        ui = UI()

        while self.mode == "Launch Prep":
            if self.control.get_action_group(9):
                self.control.throttle = 1
                self.stage()
                self.mode = "Launch"

        while self.mode != "Orbit":
            self.pitch_and_heading()

            if self.falafels is True:
                if self.altitude() > 80000:
                    self.control.toggle_action_group(8)
                    self.falafels = False

            if self.mode == "Launch":
                _twr = self.twr_calc(self.thrust(), self.mass(), self.altitude(), self.radius_eq, self.mu)
                if _twr > 1:
                    self.lAz_data = self.azimuth_init()
                    self.stage()
                    self.mode = "Booster"

            if self.mode == "Booster":
                self.flameout("Core Stage")

            if self.mode == "Core Stage":
                self.flameout("Orbit Insertion")

            if self.mode == "Orbit Insertion":
                if (self.circ_dv() < 10) or (_tp < self.period()):
                    self.control.throttle = 0
                    self.mode = "Orbit"

            if self.circ_dv() > 500: time.sleep(.1)
            ui.gravity_turn(self.mode)

        ui.remove_ui()
        self.launch_final()


class LunarTransfer(LunarXFerManager):
    def __init__(self):
        super().__init__()

        self.camera.mode = self.CameraMode.free

    def transfer(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #               L U N A R                #
        #            T R A N S F E R             #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.xfer_setup()
        self.KSC.warp_to(self.ut() + self.injection_ETA() - 240)
        ui = UI()

        while self.injection_ETA() > 140:
            ui.transfer(self.mode)
            time.sleep(1)

        self.ullage_rcs()
        self.control.throttle = 1

        while self.apoapsis_radius() < 400000000:
            if self.eng_status(self.get_active_engine(), "Status") == "Flame-Out!": self.stage()
            time.sleep(.1)
            ui.transfer(self.mode)

        self.control.throttle = 0


class LunarCapture(LunarXFerManager):
    def __init__(self):
        super().__init__()

    def capture(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #              L U N A R                 #
        #            C A P T U R E               #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.warp_moon()
        self.xfer_setup()
        self.control.toggle_action_group(2)

        self.capture_burn()
        self.control.throttle = 0

        self.lmo_burn()
        self.impact_burn()


class Testing(LunarXFerManager):
    def __init__(self):
        super().__init__()

    def test(self):
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        #             T E S T I N G              #
        # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        while True:
            print(np.rad2deg(self.moon_mean_anomaly()))
            time.sleep(1)


def main():
    # LaunchControl().launch()
    # LunarTransfer().transfer()
    # LunarCapture().capture()
    Testing().test()


main()
