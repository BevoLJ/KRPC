import time
from UI_Panel import FlightUI


# /todo/ comment program.


class FlightControl(FlightUI):
    def __init__(self):
        super().__init__()

    def launch(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #              L A U N C H               #
            #             P R O G R A M              #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        self.control.throttle = 1
        mode = self.launch_ui()
        ui = FlightUI()

        while mode != "Orbit":
            self.pitch_and_heading()

            if mode == "Launch":
                if self.twr() > 1:
                    self.lAz_data = self.azimuth_init()
                    self.control.activate_next_stage()
                    mode = "Booster Stage"

            if mode == "Booster Stage":

                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    mode = "Mid Stage"

            if mode == "Mid Stage":
                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    mode = "Upper Stage"

            if mode == "Upper Stage":
                if self.eng_status() == "Flame-Out!":
                    self.control.throttle = 0
                    time.sleep(1.5)
                    self.control.activate_next_stage()
                    self.control.rcs = True
                    # self.control.rcs = True
                    mode = "Cruise"

            if mode == "Cruise":
                if self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 2:
                    mode = "Orbital Insertion"

            if mode == "Orbital Insertion":
                self.control.rcs = False
                self.control.throttle = 1
                if self.circ_dv() < 50:
                    mode = "Orbit"

            if self.circ_dv() < 500:
                time.sleep(.01)
            else:
                time.sleep(.075)

            ui.gravity_turn(mode)

        self.control.throttle = 0

    def lunar_xfer(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #            T R A N S F E R             #
            #             P R O G R A M              #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.control.throttle = 0


def main():
    FlightControl().launch()
    # FlightControl().lunar_xfer()
    # Testing().test()
    # launch_ui()
    # flight_ui_testing()


main()
