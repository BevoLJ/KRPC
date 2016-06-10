import time
import numpy as np
from Launch_UI import LaunchUI
from Transfer_UI import TransferUI


class LaunchControl(LaunchUI):
    def __init__(self):
        super().__init__()

        self.mode = "Launch Prep"
        # self.mode = "Cruise"

    def launch(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #              L A U N C H               #
            #             P R O G R A M              #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        # print("For 250km Parking Orbit - Moon Shot launch at LAN = 353.55846")
        print("For 400km Parking Orbit - Moon Shot launch at LAN = 334.56846")
        # self.control.throttle = 1
        ui = LaunchUI()

        while self.mode == "Launch Prep":
            if self.control.get_action_group(9): self.mode = "Launch"; self.control.activate_next_stage()
            time.sleep(1)

        while self.mode != "Orbit":
            self.pitch_and_heading()

            if self.mode == "Launch":
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
                    self.mode = "Insertion"

            if self.mode == "Insertion":
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


class LunarTransfer(TransferUI):
    def __init__(self):
        super().__init__()

        self.mode = "LEO Cruise"

    def transfer(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #               L U N A R                #
            #            T R A N S F E R             #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        # self.ap.reference_frame = self.vessel.orbital_reference_frame
        # self.ap.target_direction = (0, 1, 0)
        # self.ap.engage()
        # ui = TransferUI()
        # d = 2
        # h = 4
        # m = 38
        print("XFer:      " + str(self.seconds_finder(2, 4, 38)))
        print(np.rad2deg(self.moon_future_mean(self.ut() + self.seconds_finder(2, 4, 38))))

        # while self.mode != "XFer Complete":
        #     ui.transfer_ui("LEO Cruise")
        #     time.sleep(.1)


def main():
    LaunchControl().launch()
    LunarTransfer().transfer()

main()
