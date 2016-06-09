import time
from Launch_UI import LaunchUI
from Transfer_UI import TransferUI


class LaunchControl(LaunchUI):
    def __init__(self):
        super().__init__()

        self.mode = self.launch_ui()

    def launch(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #              L A U N C H               #
            #             P R O G R A M              #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        self.control.throttle = 1
        ui = LaunchUI()

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
                if self.eng_status() == "Flame-Out!":
                    self.control.throttle = 0
                    time.sleep(1.5)
                    self.control.activate_next_stage()
                    self.control.rcs = True
                    self.mode = "Cruise"

            if self.mode == "Cruise":
                if self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 5:
                    self.mode = "Insertion"

            if self.mode == "Insertion":
                self.control.rcs = False
                self.control.throttle = 1
                if (self.circ_dv() < 30) or (self.orbital_period(250000 + self.radius_eq, self.mu) < self.period()):
                    self.control.throttle = 0
                    self.mode = "Orbit"

            if self.circ_dv() > 500:
                time.sleep(.1)

            ui.gravity_turn(self.mode)

        self.control.rcs = True
        self.ap.disengage()
        self.control.sas = True
        time.sleep(2)


class LunarTransfer(TransferUI):
    def __init__(self):
        super().__init__()

    def transfer(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #               L U N A R                #
            #            T R A N S F E R             #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        # self.ap.engage()
        # ui = TransferUI()

        while self.mode != "XFer":
            print("To The Moon!")


def main():
    LaunchControl().launch()
    LunarTransfer().transfer()

main()
