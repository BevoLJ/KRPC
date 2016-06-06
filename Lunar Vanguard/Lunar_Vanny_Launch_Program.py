import time
from Launch_UI import LaunchUI


# /todo/ comment program.


class LaunchControl(LaunchUI):
    def __init__(self):
        super().__init__()

        self.eccentricity = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')

    def launch(self):
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
            #              L A U N C H               #
            #             P R O G R A M              #
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

        self.ap.engage()
        self.control.throttle = 1
        mode = self.launch_ui()
        ui = LaunchUI()
        _ecc = self.eccentricity()
        _ecc_new = _ecc

        while mode != "Orbit":
            self.pitch_and_heading()

            if mode == "Launch":
                _twr = self.twr_calc(self.thrust(), self.mass(), self.altitude(), self.radius_eq, self.mu)
                if _twr > 1:
                    self.lAz_data = self.azimuth_init()
                    self.control.activate_next_stage()
                    mode = "Booster Stage"

            if mode == "Booster Stage":

                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    time.sleep(1.5)
                    mode = "Mid Stage"

            if mode == "Mid Stage":
                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    time.sleep(1.5)
                    mode = "Upper Stage"

            if mode == "Upper Stage":
                if self.eng_status() == "Flame-Out!":
                    self.control.throttle = 0
                    time.sleep(1.5)
                    self.control.activate_next_stage()
                    self.control.rcs = True
                    mode = "Cruise"

            if mode == "Cruise":
                if self.time_to_burn(self.ETA_ap(), self.maneuver_burn_time(self.circ_dv())) < 2:
                    mode = "Orbital Insertion"

            if mode == "Orbital Insertion":
                self.control.rcs = False
                self.control.throttle = 1
                if self.circ_dv() < 15 or _ecc > _ecc_new:
                    mode = "Orbit"
                _ecc_new = _ecc

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
    LaunchControl().launch()
    # LaunchControl().lunar_xfer()
    # Testing().test()
    # launch_ui()
    # flight_ui_testing()


main()
