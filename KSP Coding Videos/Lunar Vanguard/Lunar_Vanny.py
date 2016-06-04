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
        self.ap.target_pitch_and_heading(90, 90)
        mode = self.launch_ui()
        ui = FlightUI()

        while mode != "Orbit":

            if mode == "Launch":
                if self.twr() > 1:
                    self.ap.target_pitch_and_heading(90, 90)
                    self.control.activate_next_stage()
                    mode = "Booster Stage"

            if mode == "Booster Stage":
                if self.vessel_speed() < 80:
                    self.ap.target_pitch_and_heading(90, 90)
                else:
                    self.ap.target_pitch_and_heading(self.pitch(), self.azimuth_init())

                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    mode = "Mid Stage"

            if mode == "Mid Stage":
                if self.vessel_speed() < 2200 or (self.apoapsis_altitude() < (self.target_orbit_alt * .92)):
                    self.ap.target_pitch_and_heading(self.pitch(), 90)
                else:
                    self.ap.target_pitch_and_heading(self.target_apoapsis_speed_dv() / 3.5, self.azimuth_init())
                if self.eng_status() == "Flame-Out!":
                    self.control.activate_next_stage()
                    mode = "Upper Stage"

            if mode == "Upper Stage":
                if self.vessel_speed() < 2200 or (self.apoapsis_altitude() < (self.target_orbit_alt * .92)):
                    self.ap.target_pitch_and_heading(self.pitch(), 90)
                else:
                    self.ap.target_pitch_and_heading(self.target_apoapsis_speed_dv() / 3.5, self.azimuth_init())
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
                self.ap.target_pitch_and_heading(self.target_apoapsis_speed_dv(), self.azimuth_init())
                if self.circ_dv() < 50:
                    mode = "Orbit"

            if self.circ_dv() < 500:
                time.sleep(.01)
            else:
                time.sleep(.2)

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
